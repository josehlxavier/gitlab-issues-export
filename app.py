import requests
from bs4 import BeautifulSoup
import re
import json
import time
from urllib.parse import urljoin
from datetime import datetime

class GitLabIssueExtractor:
    def __init__(self, base_url="https://gitlab.com"):
        self.base_url = base_url
        self.session = requests.Session()
        # Adicionar headers para parecer mais com um browser real
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def fetch_page(self, url):
        """Busca uma página e retorna o HTML"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Erro ao buscar {url}: {e}")
            return None

    def extract_issue_links_from_list(self, html):
        """Extrai os links das issues da página de listagem"""
        soup = BeautifulSoup(html, 'html.parser')
        issue_links = []
        
        # Procurar por links que apontam para issues específicas
        issue_pattern = re.compile(r'/issues/\d+$')
        
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if href and issue_pattern.search(href):
                full_url = urljoin(self.base_url, href)
                if full_url not in issue_links:
                    issue_links.append(full_url)
        
        return issue_links

    def extract_issue_details(self, issue_url):
        """Extrai detalhes de uma issue específica"""
        html = self.fetch_page(issue_url)
        if not html:
            return None
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Estrutura básica do resultado
        issue_data = {
            'url': issue_url,
            'id': None,
            'title': None,
            'description': None,
            'author': None,
            'created_date': None,
            'updated_date': None,
            'state': None,
            'labels': [],
            'assignees': [],
            'comments': []
        }
        
        try:
            # Extrair ID da issue
            id_match = re.search(r'/issues/(\d+)', issue_url)
            if id_match:
                issue_data['id'] = id_match.group(1)
            
            # Extrair título
            title_element = soup.find('h1', class_='title')
            if title_element:
                issue_data['title'] = title_element.get_text(strip=True)
            
            # Extrair descrição
            desc_element = soup.find('div', class_='description')
            if desc_element:
                issue_data['description'] = desc_element.get_text(strip=True)
            
            # Extrair autor
            author_element = soup.find('span', class_='author')
            if author_element:
                author_link = author_element.find('a')
                if author_link:
                    issue_data['author'] = author_link.get_text(strip=True)
            
            # Extrair datas (pode variar dependendo da estrutura da página)
            time_elements = soup.find_all('time')
            for time_elem in time_elements:
                datetime_attr = time_elem.get('datetime')
                if datetime_attr:
                    if 'created' in time_elem.get('title', '').lower():
                        issue_data['created_date'] = datetime_attr
                    elif 'updated' in time_elem.get('title', '').lower():
                        issue_data['updated_date'] = datetime_attr
            
            # Extrair estado
            state_element = soup.find('span', class_='state-badge')
            if state_element:
                issue_data['state'] = state_element.get_text(strip=True)
            
            # Extrair labels
            label_elements = soup.find_all('span', class_='badge')
            for label_elem in label_elements:
                label_text = label_elem.get_text(strip=True)
                if label_text and label_text not in issue_data['labels']:
                    issue_data['labels'].append(label_text)
                    
        except Exception as e:
            print(f"Erro ao processar issue {issue_url}: {e}")
        
        return issue_data

    def extract_all_issues(self, issues_list_url, delay=1):
        """Extrai informações de todas as issues da página de listagem"""
        print(f"Buscando página de issues: {issues_list_url}")
        html = self.fetch_page(issues_list_url)
        
        if not html:
            print("Erro: Não foi possível buscar a página de issues")
            return []
        
        # Extrair links das issues
        issue_links = self.extract_issue_links_from_list(html)
        print(f"Encontradas {len(issue_links)} issues")
        
        all_issues = []
        
        for i, issue_url in enumerate(issue_links, 1):
            print(f"Processando issue {i}/{len(issue_links)}: {issue_url}")
            
            issue_data = self.extract_issue_details(issue_url)
            if issue_data:
                all_issues.append(issue_data)
            
            # Delay para evitar sobrecarga do servidor
            if delay > 0:
                time.sleep(delay)
        
        return all_issues

    def save_to_json(self, issues_data, filename):
        """Salva os dados das issues em um arquivo JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(issues_data, f, indent=2, ensure_ascii=False)
            print(f"Dados salvos em {filename}")
        except Exception as e:
            print(f"Erro ao salvar arquivo: {e}")

    def print_summary(self, issues_data):
        """Imprime um resumo das issues extraídas"""
        print(f"\n=== RESUMO ===")
        print(f"Total de issues extraídas: {len(issues_data)}")
        
        for issue in issues_data[:5]:  # Mostrar apenas as primeiras 5
            print(f"\nIssue #{issue['id']}: {issue['title'][:80]}...")
            print(f"  Autor: {issue['author']}")
            print(f"  Estado: {issue['state']}")
            print(f"  URL: {issue['url']}")

if __name__ == "__main__":
    # URL da página de issues
    issues_url = "https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues?sort=created_date&state=opened&first_page_size=50"
    
    # Criar extrator
    extractor = GitLabIssueExtractor()
    
    # Extrair todas as issues
    issues = extractor.extract_all_issues(issues_url, delay=2)  # 2 segundos de delay entre requests
    
    if issues:
        # Salvar em arquivo JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gitlab_issues_{timestamp}.json"
        extractor.save_to_json(issues, filename)
        
        # Mostrar resumo
        extractor.print_summary(issues)
    else:
        print("Nenhuma issue foi extraída.")
