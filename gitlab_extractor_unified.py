#!/usr/bin/env python3
"""
GitLab Issues Extractor - Script Unificado
Extrai informações de issues do GitLab usando a API pública com múltiplas opções de saída e filtros
"""

import requests
import json
import time
import argparse
import csv
import re
import os
from datetime import datetime
from urllib.parse import quote, urljoin
from pathlib import Path

class GitLabIssuesExtractor:
    def __init__(self, base_url="https://gitlab.com", output_base_dir="reports"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v4"
        self.output_base_dir = output_base_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Criar diretórios de saída se não existirem
        self.directories = {
            'json': Path(self.output_base_dir) / 'json',
            'csv': Path(self.output_base_dir) / 'csv', 
            'markdown': Path(self.output_base_dir) / 'markdown',
            'summary': Path(self.output_base_dir) / 'summary'
        }
        
        for directory in self.directories.values():
            directory.mkdir(parents=True, exist_ok=True)

    def get_project_issues(self, project_path, state='opened', per_page=50, page=1, labels=None):
        """Busca issues de um projeto usando a API pública do GitLab"""
        encoded_project = quote(project_path, safe='')
        url = f"{self.api_url}/projects/{encoded_project}/issues"
        
        params = {
            'state': state,
            'per_page': per_page,
            'page': page,
            'order_by': 'created_at',
            'sort': 'desc'
        }
        
        # Adicionar filtro por labels se especificado
        if labels:
            params['labels'] = ','.join(labels)
        
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

    def get_issue_notes(self, project_path, issue_iid):
        """Busca comentários/notas de uma issue"""
        encoded_project = quote(project_path, safe='')
        url = f"{self.api_url}/projects/{encoded_project}/issues/{issue_iid}/notes"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if self.verbose:
                print(f"Erro ao buscar comentários da issue {issue_iid}: {e}")
            return []

    def filter_issues_by_labels(self, issues, include_labels=None, exclude_labels=None):
        """Filtra issues por labels incluir/excluir"""
        if not include_labels and not exclude_labels:
            return issues
        
        filtered_issues = []
        
        for issue in issues:
            issue_labels = [label.lower() for label in issue.get('labels', [])]
            
            # Verificar labels a incluir
            if include_labels:
                include_match = any(
                    any(inc_label.lower() in issue_label for issue_label in issue_labels)
                    for inc_label in include_labels
                )
                if not include_match:
                    continue
            
            # Verificar labels a excluir
            if exclude_labels:
                exclude_match = any(
                    any(exc_label.lower() in issue_label for issue_label in issue_labels)
                    for exc_label in exclude_labels
                )
                if exclude_match:
                    continue
            
            filtered_issues.append(issue)
        
        return filtered_issues

    def extract_all_issues(self, project_path, state='opened', max_pages=5, 
                          include_comments=True, labels=None, include_labels=None, 
                          exclude_labels=None, delay=1.0, verbose=False):
        """Extrai informações detalhadas de todas as issues"""
        self.verbose = verbose
        all_issues = []
        page = 1
        
        if verbose:
            print(f"Buscando issues do projeto: {project_path}")
            if labels:
                print(f"Filtro API por labels: {labels}")
            if include_labels:
                print(f"Filtro local incluir labels: {include_labels}")
            if exclude_labels:
                print(f"Filtro local excluir labels: {exclude_labels}")
        
        while page <= max_pages:
            if verbose:
                print(f"Processando página {page}...")
            
            issues = self.get_project_issues(project_path, state=state, page=page, labels=labels)
            
            if not issues:
                if verbose:
                    print("Nenhuma issue encontrada nesta página.")
                break
            
            if verbose:
                print(f"Encontradas {len(issues)} issues na página {page}")
            
            # Aplicar filtros locais por labels
            if include_labels or exclude_labels:
                original_count = len(issues)
                issues = self.filter_issues_by_labels(issues, include_labels, exclude_labels)
                if verbose and len(issues) != original_count:
                    print(f"Filtros locais reduziram para {len(issues)} issues")
            
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
                
                # Buscar comentários se solicitado
                if include_comments and issue_data['user_notes_count'] > 0:
                    if verbose:
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
                    
                    time.sleep(0.5)  # Delay para comentários
                
                all_issues.append(issue_data)
            
            # Se retornou menos issues que o limite, chegamos ao fim
            if len(issues) < 50:
                break
                
            page += 1
            time.sleep(delay)
        
        return all_issues

    def get_standardized_filename(self, format_type, custom_name=None):
        """Gera nome padronizado do arquivo baseado na data atual"""
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        if custom_name:
            base_name = f"{custom_name}-{current_date}"
        else:
            base_name = f"gitlab-issues-{current_date}"
        
        extensions = {
            'json': '.json',
            'csv': '.csv', 
            'markdown': '.md',
            'summary': '.md'
        }
        
        filename = base_name + extensions[format_type]
        filepath = self.directories[format_type] / filename
        
        return filepath

    def save_to_json(self, issues_data, custom_name=None):
        """Salva os dados das issues em um arquivo JSON"""
        try:
            filepath = self.get_standardized_filename('json', custom_name)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(issues_data, f, indent=2, ensure_ascii=False)
            print(f"✅ Dados JSON salvos em: {filepath}")
            return str(filepath)
        except Exception as e:
            print(f"❌ Erro ao salvar arquivo JSON: {e}")
            return None

    def save_to_csv(self, issues_data, custom_name=None):
        """Salva os dados das issues em formato CSV"""
        try:
            filepath = self.get_standardized_filename('csv', custom_name)
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'id', 'iid', 'title', 'author', 'author_username', 'state',
                    'created_at', 'updated_at', 'closed_at', 'labels', 'assignees', 
                    'web_url', 'user_notes_count', 'upvotes', 'downvotes', 
                    'merge_requests_count', 'confidential', 'due_date', 'weight',
                    'description_preview', 'milestone_title'
                ]
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for issue in issues_data:
                    row = {
                        'id': issue['id'],
                        'iid': issue['iid'],
                        'title': issue['title'],
                        'author': issue['author'],
                        'author_username': issue['author_username'],
                        'state': issue['state'],
                        'created_at': issue['created_at'],
                        'updated_at': issue['updated_at'],
                        'closed_at': issue['closed_at'],
                        'labels': '; '.join(issue['labels']) if issue['labels'] else '',
                        'assignees': '; '.join(issue['assignees']) if issue['assignees'] else '',
                        'web_url': issue['web_url'],
                        'user_notes_count': issue['user_notes_count'],
                        'upvotes': issue['upvotes'],
                        'downvotes': issue['downvotes'],
                        'merge_requests_count': issue['merge_requests_count'],
                        'confidential': issue['confidential'],
                        'due_date': issue['due_date'],
                        'weight': issue['weight'],
                        'description_preview': (issue['description'][:200] + '...') if issue['description'] and len(issue['description']) > 200 else (issue['description'] or ''),
                        'milestone_title': issue['milestone']['title'] if issue['milestone'] else ''
                    }
                    writer.writerow(row)
            
            print(f"✅ Dados CSV salvos em: {filepath}")
            return str(filepath)
        except Exception as e:
            print(f"❌ Erro ao salvar arquivo CSV: {e}")
            return None

    def save_to_markdown(self, issues_data, custom_name=None):
        """Salva os dados das issues em formato Markdown detalhado"""
        try:
            filepath = self.get_standardized_filename('markdown', custom_name)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# Issues do GitLab - Relatório Detalhado\n\n")
                f.write(f"**Data da extração:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Total de issues:** {len(issues_data)}\n\n")
                
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
            
            print(f"✅ Relatório Markdown salvo em: {filepath}")
            return str(filepath)
        except Exception as e:
            print(f"❌ Erro ao salvar arquivo Markdown: {e}")
            return None

    def save_summary_report(self, issues_data, custom_name=None):
        """Cria um relatório resumido das issues extraídas"""
        try:
            filepath = self.get_standardized_filename('summary', custom_name)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("# Relatório Resumido - Issues do GitLab\n\n")
                f.write(f"**Data da extração:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Total de issues:** {len(issues_data)}\n\n")
                
                # Estatísticas gerais
                f.write("## 📊 Estatísticas Gerais\n\n")
                
                # Por estado
                states = {}
                for issue in issues_data:
                    state = issue['state']
                    states[state] = states.get(state, 0) + 1
                f.write("### Por Estado\n")
                for state, count in states.items():
                    f.write(f"- **{state.title()}:** {count} issues\n")
                f.write("\n")
                
                # Por autor
                authors = {}
                for issue in issues_data:
                    author = issue['author']
                    authors[author] = authors.get(author, 0) + 1
                
                f.write("### Top Autores\n")
                top_authors = sorted(authors.items(), key=lambda x: x[1], reverse=True)
                for author, count in top_authors[:10]:
                    f.write(f"- **{author}:** {count} issues\n")
                f.write("\n")
                
                # Por labels mais comuns
                all_labels = {}
                for issue in issues_data:
                    for label in issue['labels']:
                        all_labels[label] = all_labels.get(label, 0) + 1
                
                if all_labels:
                    f.write("### Labels Mais Comuns\n")
                    top_labels = sorted(all_labels.items(), key=lambda x: x[1], reverse=True)
                    for label, count in top_labels[:20]:
                        f.write(f"- **{label}:** {count} issues\n")
                    f.write("\n")
                
                # Lista resumida das issues
                f.write("## 📋 Lista Resumida das Issues\n\n")
                
                # Ordenar por data de criação
                issues_sorted = sorted(issues_data, key=lambda x: x['created_at'], reverse=True)
                
                for i, issue in enumerate(issues_sorted, 1):
                    f.write(f"### {i}. Issue #{issue['iid']}\n\n")
                    f.write(f"**📌 Título:** {issue['title']}\n")
                    f.write(f"**👤 Autor:** {issue['author']} (@{issue['author_username']})\n")
                    f.write(f"**📅 Criado:** {issue['created_at'][:10]} às {issue['created_at'][11:19]}\n")
                    f.write(f"**🔗 URL:** {issue['web_url']}\n")
                    f.write(f"**⚡ Estado:** {issue['state'].upper()}\n")
                    
                    if issue['labels']:
                        f.write(f"**🏷️ Labels:** {', '.join(issue['labels'])}\n")
                    
                    # Descrição resumida
                    if issue['description']:
                        desc = issue['description'].replace('\n', ' ').strip()
                        if len(desc) > 150:
                            desc = desc[:150] + "..."
                        f.write(f"**📝 Descrição:** {desc}\n")
                    
                    f.write("\n---\n\n")
            
            print(f"✅ Relatório resumido salvo em: {filepath}")
            return str(filepath)
        except Exception as e:
            print(f"❌ Erro ao salvar relatório resumido: {e}")
            return None

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
        
        # Labels mais comuns
        all_labels = {}
        for issue in issues_data:
            for label in issue['labels']:
                all_labels[label] = all_labels.get(label, 0) + 1
        
        if all_labels:
            top_labels = sorted(all_labels.items(), key=lambda x: x[1], reverse=True)[:5]
            print(f"Top 5 labels: {top_labels}")


def main():
    parser = argparse.ArgumentParser(
        description='Extrai issues do GitLab usando a API pública',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

  # Extração básica com saída JSON e resumo
  python %(prog)s --output json,summary

  # Extrair apenas issues com label específica
  python %(prog)s --labels "bug,enhancement" --output csv

  # Filtrar issues incluindo certas labels e excluindo outras  
  python %(prog)s --include-labels "bug" --exclude-labels "wontfix" --output all

  # Extração completa com todos os formatos
  python %(prog)s --state all --pages 10 --output all --include-comments

  # Extração rápida sem comentários
  python %(prog)s --no-comments --output summary --delay 0.5
        """
    )
    
    # Argumentos principais
    parser.add_argument('--project', '-p', 
                       default='raidiam-conformance/open-finance/certification',
                       help='Caminho do projeto no GitLab (formato: owner/repo)')
    
    parser.add_argument('--state', '-s', 
                       choices=['opened', 'closed', 'all'], 
                       default='opened',
                       help='Estado das issues a extrair (default: opened)')
    
    parser.add_argument('--pages', '-n', 
                       type=int, 
                       default=5,
                       help='Número máximo de páginas a processar (default: 5)')
    
    parser.add_argument('--delay', '-d', 
                       type=float, 
                       default=1.0,
                       help='Delay em segundos entre requests (default: 1.0)')
    
    # Argumentos de filtros por labels
    parser.add_argument('--labels', 
                       help='Labels específicas para filtro na API (separadas por vírgula)')
    
    parser.add_argument('--include-labels', 
                       help='Incluir apenas issues com essas labels (separadas por vírgula)')
    
    parser.add_argument('--exclude-labels', 
                       help='Excluir issues com essas labels (separadas por vírgula)')
    
    # Argumentos de saída
    parser.add_argument('--output', '-o', 
                       default='json,summary',
                       help='Formatos de saída: json, csv, markdown, summary, all (separados por vírgula)')
    
    parser.add_argument('--filename', '-f',
                       help='Nome personalizado para os arquivos (será adicionado antes da data)')
    
    parser.add_argument('--output-dir',
                       default='reports',
                       help='Diretório base para salvar os relatórios (default: reports)')
    
    # Argumentos de comportamento
    parser.add_argument('--include-comments', 
                       action='store_true',
                       help='Incluir comentários das issues (pode ser lento)')
    
    parser.add_argument('--no-comments', 
                       action='store_true',
                       help='Não buscar comentários das issues (mais rápido)')
    
    parser.add_argument('--verbose', '-v', 
                       action='store_true',
                       help='Modo verboso')
    
    args = parser.parse_args()
    
    # Processar argumentos
    include_comments = args.include_comments and not args.no_comments
    
    # Processar labels
    labels = args.labels.split(',') if args.labels else None
    include_labels = args.include_labels.split(',') if args.include_labels else None
    exclude_labels = args.exclude_labels.split(',') if args.exclude_labels else None
    
    # Processar formatos de saída
    output_formats = [fmt.strip().lower() for fmt in args.output.split(',')]
    if 'all' in output_formats:
        output_formats = ['json', 'csv', 'markdown', 'summary']
    
    # Definir nome personalizado (se fornecido)
    custom_name = args.filename if args.filename else None
    
    # Mostrar configurações se verboso
    if args.verbose:
        print("=" * 60)
        print("CONFIGURAÇÕES DA EXTRAÇÃO")
        print("=" * 60)
        print(f"Projeto: {args.project}")
        print(f"Estado: {args.state}")
        print(f"Páginas máximas: {args.pages}")
        print(f"Delay: {args.delay}s")
        print(f"Incluir comentários: {include_comments}")
        print(f"Formatos de saída: {', '.join(output_formats)}")
        print(f"Diretório de saída: {args.output_dir}")
        if custom_name:
            print(f"Nome personalizado: {custom_name}")
        if labels:
            print(f"Filtro API por labels: {labels}")
        if include_labels:
            print(f"Incluir labels: {include_labels}")
        if exclude_labels:
            print(f"Excluir labels: {exclude_labels}")
        print("=" * 60)
    
    # Criar extrator com diretório de saída personalizado
    extractor = GitLabIssuesExtractor(output_base_dir=args.output_dir)
    
    print("🚀 Iniciando extração de issues do GitLab...")
    
    # Extrair issues
    issues = extractor.extract_all_issues(
        project_path=args.project,
        state=args.state,
        max_pages=args.pages,
        include_comments=include_comments,
        labels=labels,
        include_labels=include_labels,
        exclude_labels=exclude_labels,
        delay=args.delay,
        verbose=args.verbose
    )
    
    if not issues:
        print("❌ Nenhuma issue foi extraída.")
        return False
    
    # Mostrar resumo
    extractor.print_summary(issues)
    
    # Gerar arquivos de saída
    print(f"\n📁 Gerando arquivos de saída...")
    generated_files = []
    
    if 'json' in output_formats:
        json_file = extractor.save_to_json(issues, custom_name)
        if json_file:
            generated_files.append(json_file)
    
    if 'csv' in output_formats:
        csv_file = extractor.save_to_csv(issues, custom_name)
        if csv_file:
            generated_files.append(csv_file)
    
    if 'markdown' in output_formats:
        md_file = extractor.save_to_markdown(issues, custom_name)
        if md_file:
            generated_files.append(md_file)
    
    if 'summary' in output_formats:
        summary_file = extractor.save_summary_report(issues, custom_name)
        if summary_file:
            generated_files.append(summary_file)
    
    # Relatório final
    print(f"\n✅ EXTRAÇÃO CONCLUÍDA COM SUCESSO!")
    print(f"📊 Total de issues: {len(issues)}")
    print(f"📁 Arquivos gerados:")
    for file in generated_files:
        print(f"   • {file}")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)