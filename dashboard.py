import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import subprocess
import os
import sys
from pathlib import Path
import numpy as np
from collections import Counter
import re

# Configuração da página
st.set_page_config(
    page_title="GitLab Issues Dashboard",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS customizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #f5c6cb;
    }
    .info-box {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #bee5eb;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class GitLabDashboard:
    def __init__(self):
        self.reports_dir = Path("reports")
        self.extractor_script = "gitlab_extractor_unified.py"
    
    def get_latest_json_file(self):
        """Encontra o arquivo JSON mais recente"""
        json_dir = self.reports_dir / "json"
        if not json_dir.exists():
            return None
        
        json_files = list(json_dir.glob("*.json"))
        if not json_files:
            return None
        
        return max(json_files, key=lambda x: x.stat().st_mtime)
    
    def load_issues_data(self, file_path):
        """Carrega dados das issues do arquivo JSON"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Converter para DataFrame
            df = pd.DataFrame(data)
            
            # Processar datas
            df['created_at'] = pd.to_datetime(df['created_at'])
            df['updated_at'] = pd.to_datetime(df['updated_at'])
            df['created_date'] = df['created_at'].dt.date
            df['created_hour'] = df['created_at'].dt.hour
            df['day_of_week'] = df['created_at'].dt.day_name()
            
            # Processar labels (converter de lista para string)
            df['labels_str'] = df['labels'].apply(lambda x: ', '.join(x) if isinstance(x, list) and x else 'Sem labels')
            df['labels_count'] = df['labels'].apply(lambda x: len(x) if isinstance(x, list) else 0)
            
            # Processar assignees
            df['assignees_str'] = df['assignees'].apply(lambda x: ', '.join(x) if isinstance(x, list) and x else 'Não atribuído')
            df['has_assignee'] = df['assignees'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False)
            
            return df
        except Exception as e:
            st.error(f"Erro ao carregar dados: {str(e)}")
            return None
    
    def run_extraction(self, params):
        """Executa o script de extração"""
        try:
            cmd = [sys.executable, self.extractor_script]
            
            if params.get('output'):
                cmd.extend(["--output", params['output']])
            if params.get('include_labels'):
                cmd.extend(["--include-labels", params['include_labels']])
            if params.get('exclude_labels'):
                cmd.extend(["--exclude-labels", params['exclude_labels']])
            if params.get('filename'):
                cmd.extend(["--filename", params['filename']])
            if params.get('output_dir'):
                cmd.extend(["--output-dir", params['output_dir']])
            if params.get('pages'):
                cmd.extend(["--pages", str(params['pages'])])
            if params.get('state'):
                cmd.extend(["--state", params['state']])
            
            # Adicionar --no-comments para ser mais rápido
            cmd.append("--no-comments")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                return True, "Extração concluída com sucesso!"
            else:
                return False, f"Erro na extração: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            return False, "Timeout: A extração demorou mais de 5 minutos"
        except Exception as e:
            return False, f"Erro inesperado: {str(e)}"
    
    def create_metrics_cards(self, df):
        """Cria cards com métricas principais"""
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                label="Total de Issues", 
                value=len(df),
                help="Número total de issues extraídas"
            )
        
        with col2:
            open_issues = len(df[df['state'] == 'opened'])
            closed_issues = len(df[df['state'] == 'closed'])
            delta = open_issues - closed_issues if closed_issues > 0 else open_issues
            st.metric(
                label="🟢 Issues Abertas", 
                value=open_issues,
                delta=delta,
                help="Issues atualmente abertas"
            )
        
        with col3:
            avg_comments = df['user_notes_count'].mean()
            st.metric(
                label="💬 Média Comentários", 
                value=f"{avg_comments:.1f}",
                help="Média de comentários por issue"
            )
        
        with col4:
            with_assignees = len(df[df['has_assignee']])
            percentage = (with_assignees / len(df)) * 100 if len(df) > 0 else 0
            st.metric(
                label="👥 Com Responsáveis", 
                value=with_assignees,
                delta=f"{percentage:.1f}%",
                help="Issues com responsáveis atribuídos"
            )
        
        with col5:
            avg_upvotes = df['upvotes'].mean()
            st.metric(
                label="👍 Média de Votos", 
                value=f"{avg_upvotes:.1f}",
                help="Média de votos positivos por issue"
            )
    
    def create_visualizations(self, df):
        """Cria visualizações principais"""
        
        # Primeira linha de gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribuição por estado
            state_counts = df['state'].value_counts()
            fig_state = px.pie(
                values=state_counts.values, 
                names=state_counts.index,
                title="Distribuição por Estado",
                color_discrete_map={'opened': '#28a745', 'closed': '#dc3545'}
            )
            fig_state.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_state, use_container_width=True)
        
        with col2:
            # Issues por data de criação (últimos 30 dias)
            # Criar datetime com timezone para comparação correta
            cutoff_date = pd.Timestamp.now(tz='UTC') - timedelta(days=30)
            recent_df = df[df['created_at'] >= cutoff_date]
            daily_counts = recent_df.groupby('created_date').size().reset_index()
            daily_counts.columns = ['Data', 'Quantidade']
            
            fig_timeline = px.line(
                daily_counts, 
                x='Data', 
                y='Quantidade',
                title="Issues Criadas (Últimos 30 dias)",
                markers=True
            )
            fig_timeline.update_traces(line_color='#1f77b4')
            st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Segunda linha de gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            # Top 10 autores
            author_counts = df['author'].value_counts().head(10)
            fig_authors = px.bar(
                x=author_counts.values,
                y=author_counts.index,
                orientation='h',
                title="👤 Top 10 Autores",
                labels={'x': 'Número de Issues', 'y': 'Autor'}
            )
            fig_authors.update_traces(marker_color='#ff7f0e')
            st.plotly_chart(fig_authors, use_container_width=True)
        
        with col2:
            # Distribuição por hora do dia
            hourly_dist = df.groupby('created_hour').size()
            fig_hours = px.bar(
                x=hourly_dist.index,
                y=hourly_dist.values,
                title="🕐 Distribuição por Hora do Dia",
                labels={'x': 'Hora', 'y': 'Número de Issues'}
            )
            fig_hours.update_traces(marker_color='#2ca02c')
            st.plotly_chart(fig_hours, use_container_width=True)
        
        # Terceira linha - Labels mais comuns
        st.subheader("🏷️ Labels Mais Comuns")
        
        # Extrair todas as labels
        all_labels = []
        for labels_list in df['labels']:
            if isinstance(labels_list, list):
                all_labels.extend(labels_list)
        
        if all_labels:
            label_counts = Counter(all_labels)
            top_labels = dict(label_counts.most_common(15))
            
            fig_labels = px.bar(
                x=list(top_labels.values()),
                y=list(top_labels.keys()),
                orientation='h',
                title="Top 15 Labels",
                labels={'x': 'Frequência', 'y': 'Label'}
            )
            fig_labels.update_traces(marker_color='#9467bd')
            st.plotly_chart(fig_labels, use_container_width=True)
        else:
            st.info("Nenhuma label encontrada nos dados.")

def main():
    dashboard = GitLabDashboard()
    
    # Header principal
    st.markdown('<h1 class="main-header">GitLab Issues Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar para configurações
    with st.sidebar:
        st.header("⚙️ Configurações de Extração")
        
        with st.expander("Filtros Básicos", expanded=True):
            project = st.text_input(
                "Projeto GitLab",
                value="raidiam-conformance/open-finance/certification",
                help="Formato: owner/repository"
            )
            
            state = st.selectbox(
                "Estado das Issues",
                ["opened", "closed", "all"],
                index=0,
                help="Filtrar por estado das issues"
            )
            
            pages = st.slider(
                "Páginas a processar",
                min_value=1,
                max_value=10,
                value=3,
                help="Número máximo de páginas da API para processar"
            )
        
        with st.expander("🏷️ Filtros por Labels"):
            include_labels = st.text_input(
                "Incluir Labels",
                placeholder="Bug,Enhancement",
                help="Labels para incluir (separadas por vírgula)"
            )
            
            exclude_labels = st.text_input(
                "Excluir Labels",
                placeholder="wontfix,duplicate",
                help="Labels para excluir (separadas por vírgula)"
            )
        
        with st.expander("Configurações de Saída"):
            output_format = st.selectbox(
                "Formato de Saída",
                ["json", "csv", "markdown", "summary", "all"],
                index=0,
                help="Formatos de arquivo para gerar"
            )
            
            filename = st.text_input(
                "Nome Personalizado",
                placeholder="Deixe vazio para padrão",
                help="Nome personalizado para os arquivos"
            )
        
        st.markdown("---")
        
        # Botão de extração
        if st.button("Extrair Issues", type="primary", use_container_width=True):
            params = {
                'output': output_format,
                'include_labels': include_labels if include_labels else None,
                'exclude_labels': exclude_labels if exclude_labels else None,
                'filename': filename if filename else None,
                'pages': pages,
                'state': state,
                'output_dir': 'reports'
            }
            
            with st.spinner("🔄 Extraindo issues do GitLab..."):
                success, message = dashboard.run_extraction(params)
                
                if success:
                    st.success(message)
                    st.rerun()  # Recarregar para mostrar novos dados
                else:
                    st.error(message)
        
        st.markdown("---")
        
        # Informações do sistema
        st.subheader("ℹ️ Informações")
        
        latest_file = dashboard.get_latest_json_file()
        if latest_file:
            file_time = datetime.fromtimestamp(latest_file.stat().st_mtime)
            st.info(f"📅 Última extração:\n{file_time.strftime('%d/%m/%Y %H:%M')}")
            
            file_size = latest_file.stat().st_size / 1024
            st.info(f"📦 Tamanho do arquivo:\n{file_size:.1f} KB")
        else:
            st.warning("[AVISO] Nenhum dado encontrado.\nExecute uma extração primeiro.")

    # Conteúdo principal
    latest_file = dashboard.get_latest_json_file()
    
    if latest_file is None:
        st.markdown("""
        <div class="info-box">
            <h3>Bem-vindo ao GitLab Issues Dashboard!</h3>
            <p>Para começar, configure os parâmetros na barra lateral e clique em <strong>"Extrair Issues"</strong>.</p>
            <p>O dashboard irá:</p>
            <ul>
                <li>Extrair dados das issues do GitLab</li>
                <li>Gerar visualizações interativas</li>
                <li>Mostrar métricas e estatísticas</li>
                <li>Permitir análise detalhada dos dados</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Carregar e processar dados
    with st.spinner("Carregando dados..."):
        df = dashboard.load_issues_data(latest_file)
    
    if df is None or df.empty:
        st.error("[ERRO] Não foi possível carregar os dados ou o arquivo está vazio.")
        return
    
    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Dados Detalhados", "Análises", "Arquivos"])
    
    with tab1:
        st.subheader("Visão Geral")
        
        # Métricas principais
        dashboard.create_metrics_cards(df)
        
        st.markdown("---")
        
        # Visualizações principais
        dashboard.create_visualizations(df)
    
    with tab2:
        st.subheader("Dados Detalhados")
        
        # Filtros para a tabela
        col1, col2, col3 = st.columns(3)
        
        with col1:
            state_filter = st.multiselect(
                "Filtrar por Estado",
                df['state'].unique(),
                default=df['state'].unique()
            )
        
        with col2:
            authors = df['author'].unique()
            author_filter = st.multiselect(
                "Filtrar por Autor",
                authors,
                default=authors[:10] if len(authors) > 10 else authors
            )
        
        with col3:
            # Busca textual
            search_term = st.text_input("🔍 Buscar no título", placeholder="Digite para buscar...")
        
        # Aplicar filtros
        filtered_df = df[
            (df['state'].isin(state_filter)) &
            (df['author'].isin(author_filter))
        ]
        
        if search_term:
            filtered_df = filtered_df[
                filtered_df['title'].str.contains(search_term, case=False, na=False)
            ]
        
        # Mostrar estatísticas dos filtros
        st.info(f"[INFO] Mostrando {len(filtered_df)} de {len(df)} issues")
        
        # Configurar colunas para exibição
        display_columns = [
            'iid', 'title', 'state', 'author', 'created_at', 
            'user_notes_count', 'upvotes', 'labels_str'
        ]
        
        # Renomear colunas para exibição
        column_names = {
            'iid': 'ID',
            'title': 'Título',
            'state': 'Estado',
            'author': 'Autor',
            'created_at': 'Criado em',
            'user_notes_count': 'Comentários',
            'upvotes': 'Votos',
            'labels_str': 'Labels'
        }
        
        display_df = filtered_df[display_columns].copy()
        display_df = display_df.rename(columns=column_names)
        
        # Formatar data
        display_df['Criado em'] = display_df['Criado em'].dt.strftime('%d/%m/%Y %H:%M')
        
        # Mostrar tabela
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Título": st.column_config.TextColumn("Título", width="large"),
                "Labels": st.column_config.TextColumn("Labels", width="medium"),
            }
        )
        
        # Botões de download
        col1, col2 = st.columns(2)
        
        with col1:
            csv_data = filtered_df.to_csv(index=False)
            st.download_button(
                "📥 Download CSV",
                csv_data,
                f"gitlab_issues_filtered_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                "text/csv",
                use_container_width=True
            )
        
        with col2:
            json_data = filtered_df.to_json(orient='records', date_format='iso')
            st.download_button(
                "📥 Download JSON",
                json_data,
                f"gitlab_issues_filtered_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                "application/json",
                use_container_width=True
            )
    
    with tab3:
        st.subheader("Análises Avançadas")
        
        # Análise temporal detalhada
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("📅 **Análise por Dia da Semana**")
            day_counts = df['day_of_week'].value_counts()
            # Ordenar por ordem dos dias da semana
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_counts = day_counts.reindex([day for day in day_order if day in day_counts.index])
            
            fig_days = px.bar(
                x=day_counts.index,
                y=day_counts.values,
                title="Issues por Dia da Semana"
            )
            st.plotly_chart(fig_days, use_container_width=True)
        
        with col2:
            st.write("💬 **Análise de Comentários**")
            # Distribuição de comentários
            comment_bins = [0, 1, 5, 10, 20, float('inf')]
            comment_labels = ['0', '1-4', '5-9', '10-19', '20+']
            df['comment_range'] = pd.cut(df['user_notes_count'], bins=comment_bins, labels=comment_labels, right=False)
            
            comment_dist = df['comment_range'].value_counts()
            fig_comments = px.pie(
                values=comment_dist.values,
                names=comment_dist.index,
                title="Distribuição de Comentários"
            )
            st.plotly_chart(fig_comments, use_container_width=True)
        
        # Análise de correlações
        st.write("🔗 **Análise de Correlações**")
        
        # Criar matriz de correlação para variáveis numéricas
        numeric_columns = ['user_notes_count', 'upvotes', 'downvotes', 'merge_requests_count', 'labels_count']
        available_columns = [col for col in numeric_columns if col in df.columns]
        
        if len(available_columns) >= 2:
            corr_matrix = df[available_columns].corr()
            
            fig_corr = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                color_continuous_scale="RdBu",
                title="Matriz de Correlação"
            )
            st.plotly_chart(fig_corr, use_container_width=True)
        
        # Top issues por critérios
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("🏆 **Top Issues por Comentários**")
            top_commented = df.nlargest(10, 'user_notes_count')[['title', 'author', 'user_notes_count']]
            st.dataframe(top_commented, hide_index=True, use_container_width=True)
        
        with col2:
            st.write("👍 **Top Issues por Votos**")
            top_voted = df.nlargest(10, 'upvotes')[['title', 'author', 'upvotes']]
            st.dataframe(top_voted, hide_index=True, use_container_width=True)
    
    with tab4:
        st.subheader("Gerenciar Arquivos")
        
        # Listar todos os arquivos gerados
        reports_dir = Path("reports")
        
        if reports_dir.exists():
            for folder_name in ["json", "csv", "markdown", "summary"]:
                folder_path = reports_dir / folder_name
                
                if folder_path.exists():
                    files = list(folder_path.glob("*"))
                    
                    if files:
                        st.write(f"[PASTA] **{folder_name.upper()}** ({len(files)} arquivos)")
                        
                        for file_path in sorted(files, key=lambda x: x.stat().st_mtime, reverse=True):
                            file_size = file_path.stat().st_size / 1024
                            file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                            
                            col1, col2, col3, col4 = st.columns([3, 1, 2, 1])
                            
                            with col1:
                                st.text(f"📄 {file_path.name}")
                            
                            with col2:
                                st.text(f"{file_size:.1f} KB")
                            
                            with col3:
                                st.text(file_time.strftime("%d/%m/%Y %H:%M"))
                            
                            with col4:
                                with open(file_path, 'rb') as f:
                                    st.download_button(
                                        "⬇️",
                                        f.read(),
                                        file_path.name,
                                        key=f"download_{folder_name}_{file_path.name}"
                                    )
                        
                        st.markdown("---")
        else:
            st.info("📂 Nenhum diretório de relatórios encontrado. Execute uma extração primeiro.")

if __name__ == "__main__":
    main()