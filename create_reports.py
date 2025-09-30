import json
from datetime import datetime

def create_summary_report(json_filename):
    """
    Cria um relatório resumido das issues extraídas
    """
    try:
        with open(json_filename, 'r', encoding='utf-8') as f:
            issues = json.load(f)
    except FileNotFoundError:
        print(f"Arquivo {json_filename} não encontrado!")
        return
    
    # Criar relatório resumido
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_filename = f"gitlab_issues_summary_{timestamp}.md"
    
    with open(summary_filename, 'w', encoding='utf-8') as f:
        f.write("# Relatório Resumido - Issues do GitLab\n\n")
        f.write(f"**Data da extração:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total de issues:** {len(issues)}\n")
        f.write(f"**Projeto:** raidiam-conformance/open-finance/certification\n\n")
        
        # Estatísticas gerais
        f.write("## 📊 Estatísticas Gerais\n\n")
        
        # Por estado
        states = {}
        for issue in issues:
            state = issue['state']
            states[state] = states.get(state, 0) + 1
        f.write("### Por Estado\n")
        for state, count in states.items():
            f.write(f"- **{state.title()}:** {count} issues\n")
        f.write("\n")
        
        # Por autor
        authors = {}
        for issue in issues:
            author = issue['author']
            authors[author] = authors.get(author, 0) + 1
        
        f.write("### Top Autores\n")
        top_authors = sorted(authors.items(), key=lambda x: x[1], reverse=True)
        for author, count in top_authors[:10]:
            f.write(f"- **{author}:** {count} issues\n")
        f.write("\n")
        
        # Por labels mais comuns
        all_labels = {}
        for issue in issues:
            for label in issue['labels']:
                all_labels[label] = all_labels.get(label, 0) + 1
        
        if all_labels:
            f.write("### Labels Mais Comuns\n")
            top_labels = sorted(all_labels.items(), key=lambda x: x[1], reverse=True)
            for label, count in top_labels[:15]:
                f.write(f"- **{label}:** {count} issues\n")
            f.write("\n")
        
        # Lista detalhada das issues
        f.write("## 📋 Lista Detalhada das Issues\n\n")
        
        # Ordenar por data de criação (mais recentes primeiro)
        issues_sorted = sorted(issues, key=lambda x: x['created_at'], reverse=True)
        
        for i, issue in enumerate(issues_sorted, 1):
            f.write(f"### {i}. Issue #{issue['iid']}\n\n")
            f.write(f"**📌 Título:** {issue['title']}\n\n")
            f.write(f"**👤 Autor:** {issue['author']} (@{issue['author_username']})\n")
            f.write(f"**📅 Criado:** {issue['created_at'][:10]} às {issue['created_at'][11:19]}\n")
            f.write(f"**🔄 Atualizado:** {issue['updated_at'][:10]} às {issue['updated_at'][11:19]}\n")
            f.write(f"**🔗 URL:** {issue['web_url']}\n")
            f.write(f"**⚡ Estado:** {issue['state'].upper()}\n")
            
            if issue['labels']:
                f.write(f"**🏷️ Labels:** {', '.join(issue['labels'])}\n")
            
            if issue['assignees']:
                f.write(f"**👥 Responsáveis:** {', '.join(issue['assignees'])}\n")
            
            # Estatísticas adicionais
            stats = []
            if issue['upvotes'] > 0:
                stats.append(f"👍 {issue['upvotes']}")
            if issue['downvotes'] > 0:
                stats.append(f"👎 {issue['downvotes']}")
            if issue['user_notes_count'] > 0:
                stats.append(f"💬 {issue['user_notes_count']} comentários")
            if issue['merge_requests_count'] > 0:
                stats.append(f"🔀 {issue['merge_requests_count']} MRs")
            
            if stats:
                f.write(f"**📈 Estatísticas:** {' | '.join(stats)}\n")
            
            # Descrição resumida (primeiras 200 caracteres)
            if issue['description']:
                desc = issue['description'].replace('\n', ' ').strip()
                if len(desc) > 200:
                    desc = desc[:200] + "..."
                f.write(f"\n**📝 Descrição:** {desc}\n")
            
            f.write("\n---\n\n")
    
    print(f"Relatório resumido salvo em: {summary_filename}")
    return summary_filename

def create_csv_export(json_filename):
    """
    Cria um arquivo CSV com os dados das issues
    """
    try:
        with open(json_filename, 'r', encoding='utf-8') as f:
            issues = json.load(f)
    except FileNotFoundError:
        print(f"Arquivo {json_filename} não encontrado!")
        return
    
    import csv
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"gitlab_issues_{timestamp}.csv"
    
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'id', 'iid', 'title', 'author', 'author_username', 'state',
            'created_at', 'updated_at', 'labels', 'assignees', 'web_url',
            'user_notes_count', 'upvotes', 'downvotes', 'merge_requests_count',
            'description_preview'
        ]
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for issue in issues:
            # Preparar dados para CSV
            row = {
                'id': issue['id'],
                'iid': issue['iid'],
                'title': issue['title'],
                'author': issue['author'],
                'author_username': issue['author_username'],
                'state': issue['state'],
                'created_at': issue['created_at'],
                'updated_at': issue['updated_at'],
                'labels': '; '.join(issue['labels']) if issue['labels'] else '',
                'assignees': '; '.join(issue['assignees']) if issue['assignees'] else '',
                'web_url': issue['web_url'],
                'user_notes_count': issue['user_notes_count'],
                'upvotes': issue['upvotes'],
                'downvotes': issue['downvotes'],
                'merge_requests_count': issue['merge_requests_count'],
                'description_preview': (issue['description'][:100] + '...') if issue['description'] and len(issue['description']) > 100 else (issue['description'] or '')
            }
            writer.writerow(row)
    
    print(f"Dados exportados para CSV: {csv_filename}")
    return csv_filename

if __name__ == "__main__":
    # Nome do arquivo JSON gerado anteriormente
    json_file = "gitlab_issues_20250930_174541.json"
    
    print("Gerando relatórios adicionais...")
    
    # Criar relatório resumido
    summary_file = create_summary_report(json_file)
    
    # Criar exportação CSV
    csv_file = create_csv_export(json_file)
    
    print("\n✅ Relatórios gerados com sucesso!")
    print(f"📊 Resumo: {summary_file}")
    print(f"📈 CSV: {csv_file}")