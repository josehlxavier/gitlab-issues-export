import requests
import json
import time
from datetime import datetime
from urllib.parse import quote

class GitLabAPIExtractor:
    def __init__(self, base_url="https://gitlab.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v4"
        self.session = requests.Session()
        # Headers para parecer mais com um browser real
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def get_project_issues(self, project_path, state='opened', per_page=50, page=1):
        """
        Busca issues de um projeto usando a API pública do GitLab
        """
        # Encode do caminho do projeto
        encoded_project = quote(project_path, safe='')
        
        # Endpoint da API
        url = f"{self.api_url}/projects/{encoded_project}/issues"
        
        params = {
            'state': state,
            'per_page': per_page,
            'page': page,
            'order_by': 'created_at',
            'sort': 'desc'
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar issues via API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Status code: {e.response.status_code}")
                print(f"Response: {e.response.text}")
            return []

    def get_issue_details(self, project_path, issue_iid):
        """
        Busca detalhes específicos de uma issue
        """
        encoded_project = quote(project_path, safe='')
        url = f"{self.api_url}/projects/{encoded_project}/issues/{issue_iid}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar detalhes da issue {issue_iid}: {e}")
            return None

    def get_issue_notes(self, project_path, issue_iid):
        """
        Busca comentários/notas de uma issue
        """
        encoded_project = quote(project_path, safe='')
        url = f"{self.api_url}/projects/{encoded_project}/issues/{issue_iid}/notes"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar comentários da issue {issue_iid}: {e}")
            return []

    def extract_all_issues_detailed(self, project_path, state='opened', max_pages=5):
        """
        Extrai informações detalhadas de todas as issues
        """
        all_issues = []
        page = 1
        
        print(f"Buscando issues do projeto: {project_path}")
        
        while page <= max_pages:
            print(f"Processando página {page}...")
            
            issues = self.get_project_issues(project_path, state=state, page=page)
            
            if not issues:
                print("Nenhuma issue encontrada nesta página.")
                break
            
            print(f"Encontradas {len(issues)} issues na página {page}")
            
            for issue in issues:
                # Dados básicos da issue
                issue_data = {
                    'id': issue.get('id'),
                    'iid': issue.get('iid'),
                    'title': issue.get('title'),
                    'description': issue.get('description'),
                    'state': issue.get('state'),
                    'created_at': issue.get('created_at'),
                    'updated_at': issue.get('updated_at'),
                    'closed_at': issue.get('closed_at'),
                    'labels': issue.get('labels', []),
                    'milestone': issue.get('milestone'),
                    'assignees': [assignee.get('name') for assignee in issue.get('assignees', [])],
                    'author': issue.get('author', {}).get('name'),
                    'author_username': issue.get('author', {}).get('username'),
                    'web_url': issue.get('web_url'),
                    'references': issue.get('references'),
                    'time_stats': issue.get('time_stats'),
                    'confidential': issue.get('confidential'),
                    'discussion_locked': issue.get('discussion_locked'),
                    'due_date': issue.get('due_date'),
                    'has_tasks': issue.get('has_tasks'),
                    'task_status': issue.get('task_status'),
                    'weight': issue.get('weight'),
                    'user_notes_count': issue.get('user_notes_count', 0),
                    'merge_requests_count': issue.get('merge_requests_count', 0),
                    'upvotes': issue.get('upvotes', 0),
                    'downvotes': issue.get('downvotes', 0),
                    'comments': []
                }
                
                # Buscar comentários se existirem
                if issue_data['user_notes_count'] > 0:
                    print(f"  Buscando {issue_data['user_notes_count']} comentários da issue #{issue_data['iid']}...")
                    comments = self.get_issue_notes(project_path, issue_data['iid'])
                    
                    for comment in comments:
                        if comment.get('system', False):
                            continue  # Pular comentários do sistema
                        
                        comment_data = {
                            'id': comment.get('id'),
                            'body': comment.get('body'),
                            'author': comment.get('author', {}).get('name'),
                            'author_username': comment.get('author', {}).get('username'),
                            'created_at': comment.get('created_at'),
                            'updated_at': comment.get('updated_at'),
                            'resolvable': comment.get('resolvable'),
                            'resolved': comment.get('resolved')
                        }
                        issue_data['comments'].append(comment_data)
                    
                    # Pequeno delay para não sobrecarregar a API
                    time.sleep(0.5)
                
                all_issues.append(issue_data)
            
            # Se retornou menos issues que o limite, chegamos ao fim
            if len(issues) < 50:
                break
                
            page += 1
            time.sleep(1)  # Delay entre páginas
        
        return all_issues

    def save_to_json(self, issues_data, filename):
        """Salva os dados das issues em um arquivo JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(issues_data, f, indent=2, ensure_ascii=False)
            print(f"Dados salvos em {filename}")
        except Exception as e:
            print(f"Erro ao salvar arquivo: {e}")

    def save_to_markdown(self, issues_data, filename):
        """Salva os dados das issues em formato Markdown"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# Issues do GitLab\n\n")
                f.write(f"Total de issues: {len(issues_data)}\n")
                f.write(f"Extraído em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for issue in issues_data:
                    f.write(f"## Issue #{issue['iid']}: {issue['title']}\n\n")
                    f.write(f"**Estado:** {issue['state']}\n")
                    f.write(f"**Autor:** {issue['author']} (@{issue['author_username']})\n")
                    f.write(f"**Criado em:** {issue['created_at']}\n")
                    f.write(f"**Atualizado em:** {issue['updated_at']}\n")
                    f.write(f"**URL:** {issue['web_url']}\n")
                    
                    if issue['labels']:
                        f.write(f"**Labels:** {', '.join(issue['labels'])}\n")
                    
                    if issue['assignees']:
                        f.write(f"**Responsáveis:** {', '.join(issue['assignees'])}\n")
                    
                    f.write(f"\n### Descrição\n\n")
                    if issue['description']:
                        f.write(f"{issue['description']}\n\n")
                    else:
                        f.write("*Sem descrição*\n\n")
                    
                    if issue['comments']:
                        f.write(f"### Comentários ({len(issue['comments'])})\n\n")
                        for i, comment in enumerate(issue['comments'], 1):
                            f.write(f"#### Comentário {i} - {comment['author']} (@{comment['author_username']})\n")
                            f.write(f"*{comment['created_at']}*\n\n")
                            f.write(f"{comment['body']}\n\n")
                    
                    f.write("---\n\n")
            
            print(f"Dados salvos em {filename}")
        except Exception as e:
            print(f"Erro ao salvar arquivo markdown: {e}")

    def print_summary(self, issues_data):
        """Imprime um resumo das issues extraídas"""
        print(f"\n=== RESUMO DA EXTRAÇÃO ===")
        print(f"Total de issues extraídas: {len(issues_data)}")
        
        # Estatísticas por estado
        states = {}
        for issue in issues_data:
            state = issue['state']
            states[state] = states.get(state, 0) + 1
        
        print(f"Por estado: {states}")
        
        # Estatísticas por autor
        authors = {}
        for issue in issues_data:
            author = issue['author']
            authors[author] = authors.get(author, 0) + 1
        
        top_authors = sorted(authors.items(), key=lambda x: x[1], reverse=True)[:5]
        print(f"Top 5 autores: {top_authors}")
        
        # Mostrar algumas issues de exemplo
        print(f"\n=== EXEMPLOS DE ISSUES ===")
        for i, issue in enumerate(issues_data[:3], 1):
            print(f"\n{i}. Issue #{issue['iid']}: {issue['title'][:80]}...")
            print(f"   Autor: {issue['author']}")
            print(f"   Estado: {issue['state']}")
            print(f"   Criado: {issue['created_at']}")
            print(f"   Comentários: {len(issue['comments'])}")
            print(f"   URL: {issue['web_url']}")

if __name__ == "__main__":
    # Configurações
    project_path = "raidiam-conformance/open-finance/certification"
    
    # Criar extrator
    extractor = GitLabAPIExtractor()
    
    print("Iniciando extração de issues do GitLab...")
    print(f"Projeto: {project_path}")
    
    # Extrair issues abertas
    issues = extractor.extract_all_issues_detailed(
        project_path, 
        state='opened',  # 'opened', 'closed', 'all'
        max_pages=3      # Limitar para não sobrecarregar
    )
    
    if issues:
        # Gerar timestamp para arquivos
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Salvar em JSON
        json_filename = f"gitlab_issues_{timestamp}.json"
        extractor.save_to_json(issues, json_filename)
        
        # Salvar em Markdown
        md_filename = f"gitlab_issues_{timestamp}.md"
        extractor.save_to_markdown(issues, md_filename)
        
        # Mostrar resumo
        extractor.print_summary(issues)
        
        print(f"\n=== ARQUIVOS GERADOS ===")
        print(f"JSON: {json_filename}")
        print(f"Markdown: {md_filename}")
        
    else:
        print("Nenhuma issue foi extraída.")