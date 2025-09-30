#!/usr/bin/env python3
"""
GitLab Issues Extractor - Versão Configurável
Extrai informações de issues do GitLab usando a API pública
"""

import requests
import json
import time
import argparse
from datetime import datetime
from urllib.parse import quote

def main():
    parser = argparse.ArgumentParser(description='Extrai issues do GitLab usando a API pública')
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
    parser.add_argument('--output', '-o', 
                       help='Nome base dos arquivos de saída (default: gitlab_issues_TIMESTAMP)')
    parser.add_argument('--no-comments', 
                       action='store_true',
                       help='Não tentar buscar comentários das issues')
    parser.add_argument('--verbose', '-v', 
                       action='store_true',
                       help='Modo verboso')
    
    args = parser.parse_args()
    
    # Configurar nome de saída
    if args.output:
        output_base = args.output
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_base = f"gitlab_issues_{timestamp}"
    
    # Criar extrator com configurações
    from gitlab_api_extractor import GitLabAPIExtractor
    extractor = GitLabAPIExtractor()
    
    if args.verbose:
        print(f"Configurações:")
        print(f"  Projeto: {args.project}")
        print(f"  Estado: {args.state}")
        print(f"  Páginas máximas: {args.pages}")
        print(f"  Delay: {args.delay}s")
        print(f"  Buscar comentários: {not args.no_comments}")
        print(f"  Arquivo base: {output_base}")
        print()
    
    # Override do método para não buscar comentários se especificado
    if args.no_comments:
        def extract_all_issues_no_comments(self, project_path, state='opened', max_pages=5):
            all_issues = []
            page = 1
            
            print(f"Buscando issues do projeto: {project_path}")
            
            while page <= max_pages:
                if args.verbose:
                    print(f"Processando página {page}...")
                
                issues = self.get_project_issues(project_path, state=state, page=page)
                
                if not issues:
                    print("Nenhuma issue encontrada nesta página.")
                    break
                
                print(f"Encontradas {len(issues)} issues na página {page}")
                
                for issue in issues:
                    # Dados básicos da issue (sem comentários)
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
                        'comments': []  # Vazio quando não buscar comentários
                    }
                    
                    all_issues.append(issue_data)
                
                # Se retornou menos issues que o limite, chegamos ao fim
                if len(issues) < 50:
                    break
                    
                page += 1
                time.sleep(args.delay)
            
            return all_issues
        
        # Substituir método
        extractor.extract_all_issues_detailed = extract_all_issues_no_comments.__get__(extractor, GitLabAPIExtractor)
    
    # Extrair issues
    print("Iniciando extração de issues do GitLab...")
    print(f"Projeto: {args.project}")
    
    issues = extractor.extract_all_issues_detailed(
        args.project, 
        state=args.state,
        max_pages=args.pages
    )
    
    if issues:
        # Salvar arquivos
        json_filename = f"{output_base}.json"
        md_filename = f"{output_base}.md"
        
        extractor.save_to_json(issues, json_filename)
        extractor.save_to_markdown(issues, md_filename)
        extractor.print_summary(issues)
        
        print(f"\n=== ARQUIVOS GERADOS ===")
        print(f"JSON: {json_filename}")
        print(f"Markdown: {md_filename}")
        
        # Gerar relatórios adicionais
        if args.verbose:
            print("\nGerando relatórios adicionais...")
            
            # Criar relatório resumido
            try:
                from create_reports import create_summary_report, create_csv_export
                summary_file = create_summary_report(json_filename)
                csv_file = create_csv_export(json_filename)
                print(f"Resumo: {summary_file}")
                print(f"CSV: {csv_file}")
            except ImportError:
                print("Módulo create_reports não encontrado, pulando relatórios adicionais.")
        
        return True
    else:
        print("Nenhuma issue foi extraída.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)