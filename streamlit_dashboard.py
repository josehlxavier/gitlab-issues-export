import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import subprocess
import os
import glob
from pathlib import Path
import time

# Configuração da página
st.set_page_config(
    page_title="GitLab Issues Dashboard",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff6b6b;
    }
    .success-card {
        background-color: #d4edda;
        border-color: #c3e6cb;
        color: #155724;
    }
    .error-card {
        background-color: #f8d7da;
        border-color: #f5c6cb;
        color: #721c24;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

class GitLabDashboard:
    def __init__(self):
        self.reports_dir = Path("reports")
        self.current_data = None
        
    def ensure_reports_dir(self):
        """Garante que o diretório de relatórios existe"""
        self.reports_dir.mkdir(exist_ok=True)
        for subdir in ["json", "csv", "markdown", "summary"]:
            (self.reports_dir / subdir).mkdir(exist_ok=True)
    
    def get_latest_json_file(self):
        """Encontra o arquivo JSON mais recente"""
        json_files = list((self.reports_dir / "json").glob("*.json"))
        if json_files:
            return max(json_files, key=os.path.getctime)
        return None
    
    def load_data(self, file_path=None):
        """Carrega dados do arquivo JSON"""
        if file_path is None:
            file_path = self.get_latest_json_file()
        
        if file_path and file_path.exists():
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
                df['created_weekday'] = df['created_at'].dt.day_name()
                
                # Processar labels - converter lista de strings para string concatenada
                df['labels_str'] = df['labels'].apply(lambda x: ', '.join(x) if isinstance(x, list) else '')
                df['labels_count'] = df['labels'].apply(lambda x: len(x) if isinstance(x, list) else 0)
                
                # Processar assignees
                df['assignees_str'] = df['assignees'].apply(lambda x: ', '.join(x) if isinstance(x, list) else '')
                df['assignees_count'] = df['assignees'].apply(lambda x: len(x) if isinstance(x, list) else 0)
                
                self.current_data = df
                return df, file_path
                
            except Exception as e:
                st.error(f"Erro ao carregar dados: {str(e)}")
                return None, None
        
        return None, None
    
    def run_extraction(self, params):
        """Executa a extração de issues"""
        cmd = ["python", "gitlab_extractor_unified.py"]
        
        # Adicionar parâmetros
        if params.get('output'):
            cmd.extend(["--output", params['output']])
        if params.get('include_labels'):
            cmd.extend(["--include-labels", params['include_labels']])
        if params.get('exclude_labels'):
            cmd.extend(["--exclude-labels", params['exclude_labels']])
        if params.get('filename'):
            cmd.extend(["--filename", params['filename']])
        if params.get('state'):
            cmd.extend(["--state", params['state']])
        if params.get('pages'):
            cmd.extend(["--pages", str(params['pages'])])
        if params.get('no_comments'):
            cmd.append("--no-comments")
        
        return subprocess.run(cmd, capture_output=True, text=True)

def main():
    dashboard = GitLabDashboard()
    dashboard.ensure_reports_dir()
    
    # Título principal
    st.title("🔍 GitLab Issues Dashboard")
    st.markdown("---")
    
    # Sidebar para controles
    with st.sidebar:
        st.header("⚙️ Controles")
        
        # Seção de extração
        st.subheader("📥 Nova Extração")
        
        with st.expander("Configurar Extração", expanded=False):
            output_format = st.selectbox(
                "Formato de Saída",
                ["json,summary", "all", "json", "csv", "markdown", "summary"],
                help="Escolha quais formatos de arquivo gerar"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                state = st.selectbox("Estado", ["opened", "closed", "all"])
            with col2:
                pages = st.number_input("Páginas", min_value=1, max_value=20, value=3)
            
            include_labels = st.text_input(
                "Incluir Labels", 
                placeholder="Bug,Enhancement",
                help="Labels separadas por vírgula"
            )
            
            exclude_labels = st.text_input(
                "Excluir Labels", 
                placeholder="wontfix,duplicate",
                help="Labels separadas por vírgula"
            )
            
            filename = st.text_input(
                "Nome do Arquivo", 
                placeholder="Deixe vazio para padrão",
                help="Nome personalizado para os arquivos"
            )
            
            no_comments = st.checkbox("Pular Comentários", value=True, help="Mais rápido")
            
            if st.button("🚀 Extrair Issues", type="primary"):
                params = {
                    'output': output_format,
                    'include_labels': include_labels or None,
                    'exclude_labels': exclude_labels or None,
                    'filename': filename or None,
                    'state': state,
                    'pages': pages,
                    'no_comments': no_comments
                }
                
                with st.spinner("🔄 Extraindo issues... Isso pode levar alguns minutos."):
                    result = dashboard.run_extraction(params)
                    
                    if result.returncode == 0:
                        st.success("✅ Extração concluída!")
                        st.rerun()
                    else:
                        st.error(f"❌ Erro na extração: {result.stderr}")
        
        st.markdown("---")
        
        # Seção de arquivos
        st.subheader("📁 Arquivos Disponíveis")
        
        json_files = list((dashboard.reports_dir / "json").glob("*.json"))
        if json_files:
            # Ordenar por data de modificação (mais recente primeiro)
            json_files.sort(key=os.path.getctime, reverse=True)
            
            file_options = {}
            for file_path in json_files:
                file_name = file_path.name
                file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                display_name = f"{file_name} ({file_time.strftime('%d/%m %H:%M')})"
                file_options[display_name] = file_path
            
            selected_file_display = st.selectbox(
                "Selecionar Arquivo",
                list(file_options.keys()),
                help="Escolha qual arquivo de dados usar"
            )
            
            selected_file = file_options[selected_file_display]
            
            if st.button("🔄 Recarregar Dados"):
                st.rerun()
        else:
            st.info("👆 Nenhum arquivo encontrado. Execute uma extração primeiro!")
            selected_file = None
    
    # Área principal
    if selected_file or dashboard.get_latest_json_file():
        data, file_path = dashboard.load_data(selected_file)
        
        if data is not None:
            # Informações do arquivo
            file_info = f"📄 **Arquivo:** {file_path.name}"
            file_time = datetime.fromtimestamp(os.path.getctime(file_path))
            file_info += f" | 🕒 **Gerado:** {file_time.strftime('%d/%m/%Y às %H:%M')}"
            file_info += f" | 📊 **Issues:** {len(data)}"
            
            st.info(file_info)
            
            # Métricas principais
            st.subheader("📊 Visão Geral")
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Total de Issues", len(data))
            
            with col2:
                opened_count = len(data[data['state'] == 'opened'])
                st.metric("Issues Abertas", opened_count)
            
            with col3:
                closed_count = len(data[data['state'] == 'closed'])
                st.metric("Issues Fechadas", closed_count)
            
            with col4:
                avg_comments = data['user_notes_count'].mean()
                st.metric("Média Comentários", f"{avg_comments:.1f}")
            
            with col5:
                with_assignees = len(data[data['assignees_count'] > 0])
                st.metric("Com Responsáveis", with_assignees)
            
            # Tabs para diferentes visualizações
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📈 Análises", "📋 Dados Brutos", "👥 Autores", "🏷️ Labels", "⏰ Temporal"
            ])
            
            with tab1:
                st.subheader("📈 Análises Principais")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Gráfico de pizza - Estado das issues
                    state_counts = data['state'].value_counts()
                    fig_state = px.pie(
                        values=state_counts.values, 
                        names=state_counts.index,
                        title="Distribuição por Estado",
                        color_discrete_map={'opened': '#ff6b6b', 'closed': '#51cf66'}
                    )
                    st.plotly_chart(fig_state, use_container_width=True)
                
                with col2:
                    # Gráfico de barras - Top 10 autores
                    top_authors = data['author'].value_counts().head(10)
                    fig_authors = px.bar(
                        x=top_authors.values,
                        y=top_authors.index,
                        orientation='h',
                        title="Top 10 Autores",
                        labels={'x': 'Número de Issues', 'y': 'Autor'}
                    )
                    fig_authors.update_layout(yaxis={'categoryorder': 'total ascending'})
                    st.plotly_chart(fig_authors, use_container_width=True)
                
                # Gráfico de linha - Timeline de criação
                st.subheader("📅 Timeline de Criação")
                daily_counts = data.groupby('created_date').size().reset_index()
                daily_counts.columns = ['Data', 'Quantidade']
                
                fig_timeline = px.line(
                    daily_counts,
                    x='Data',
                    y='Quantidade',
                    title="Issues Criadas por Data",
                    markers=True
                )
                fig_timeline.update_layout(xaxis_title="Data", yaxis_title="Número de Issues")
                st.plotly_chart(fig_timeline, use_container_width=True)
                
                # Distribuição por comentários
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_comments = px.histogram(
                        data,
                        x='user_notes_count',
                        nbins=20,
                        title="Distribuição de Comentários",
                        labels={'user_notes_count': 'Número de Comentários', 'count': 'Frequência'}
                    )
                    st.plotly_chart(fig_comments, use_container_width=True)
                
                with col2:
                    # Scatter plot - Comentários vs Votos
                    fig_scatter = px.scatter(
                        data,
                        x='user_notes_count',
                        y='upvotes',
                        color='state',
                        title="Comentários vs Votos Positivos",
                        labels={'user_notes_count': 'Comentários', 'upvotes': 'Votos Positivos'}
                    )
                    st.plotly_chart(fig_scatter, use_container_width=True)
            
            with tab2:
                st.subheader("📋 Dados Brutos")
                
                # Filtros
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    state_filter = st.multiselect(
                        "Filtrar por Estado",
                        data['state'].unique(),
                        default=data['state'].unique()
                    )
                
                with col2:
                    authors = data['author'].unique()
                    author_filter = st.multiselect(
                        "Filtrar por Autor",
                        authors,
                        default=[]
                    )
                
                with col3:
                    # Filtro por data
                    min_date = data['created_date'].min()
                    max_date = data['created_date'].max()
                    
                    date_range = st.date_input(
                        "Filtrar por Data de Criação",
                        value=(min_date, max_date),
                        min_value=min_date,
                        max_value=max_date
                    )
                
                # Aplicar filtros
                filtered_data = data[data['state'].isin(state_filter)]
                
                if author_filter:
                    filtered_data = filtered_data[filtered_data['author'].isin(author_filter)]
                
                if len(date_range) == 2:
                    start_date, end_date = date_range
                    filtered_data = filtered_data[
                        (filtered_data['created_date'] >= start_date) &
                        (filtered_data['created_date'] <= end_date)
                    ]
                
                st.write(f"📊 Mostrando {len(filtered_data)} de {len(data)} issues")
                
                # Tabela de dados
                display_columns = [
                    'iid', 'title', 'state', 'author', 'created_at', 'updated_at',
                    'labels_str', 'assignees_str', 'user_notes_count', 'upvotes'
                ]
                
                display_data = filtered_data[display_columns].copy()
                display_data['created_at'] = display_data['created_at'].dt.strftime('%d/%m/%Y %H:%M')
                display_data['updated_at'] = display_data['updated_at'].dt.strftime('%d/%m/%Y %H:%M')
                
                st.dataframe(
                    display_data,
                    use_container_width=True,
                    column_config={
                        'iid': 'ID',
                        'title': st.column_config.TextColumn('Título', width='large'),
                        'state': 'Estado',
                        'author': 'Autor',
                        'created_at': 'Criado em',
                        'updated_at': 'Atualizado em',
                        'labels_str': st.column_config.TextColumn('Labels', width='medium'),
                        'assignees_str': 'Responsáveis',
                        'user_notes_count': 'Comentários',
                        'upvotes': 'Votos'
                    }
                )
                
                # Download
                csv_data = filtered_data.to_csv(index=False)
                st.download_button(
                    "📥 Download CSV Filtrado",
                    csv_data,
                    f"gitlab_issues_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    "text/csv"
                )
            
            with tab3:
                st.subheader("👥 Análise de Autores")
                
                # Estatísticas por autor
                author_stats = data.groupby('author').agg({
                    'iid': 'count',
                    'user_notes_count': 'mean',
                    'upvotes': 'sum',
                    'assignees_count': 'mean',
                    'labels_count': 'mean'
                }).round(2)
                
                author_stats.columns = [
                    'Issues Criadas', 'Média Comentários', 'Total Votos',
                    'Média Responsáveis', 'Média Labels'
                ]
                
                author_stats = author_stats.sort_values('Issues Criadas', ascending=False)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("📊 **Estatísticas por Autor**")
                    st.dataframe(author_stats, use_container_width=True)
                
                with col2:
                    # Atividade dos autores ao longo do tempo
                    author_timeline = data.groupby(['created_date', 'author']).size().reset_index()
                    author_timeline.columns = ['Data', 'Autor', 'Issues']
                    
                    top_5_authors = data['author'].value_counts().head(5).index
                    author_timeline_filtered = author_timeline[
                        author_timeline['Autor'].isin(top_5_authors)
                    ]
                    
                    fig_author_timeline = px.line(
                        author_timeline_filtered,
                        x='Data',
                        y='Issues',
                        color='Autor',
                        title="Atividade dos Top 5 Autores"
                    )
                    st.plotly_chart(fig_author_timeline, use_container_width=True)
            
            with tab4:
                st.subheader("🏷️ Análise de Labels")
                
                # Extrair todas as labels
                all_labels = []
                for labels_list in data['labels']:
                    if isinstance(labels_list, list):
                        all_labels.extend(labels_list)
                
                if all_labels:
                    labels_df = pd.DataFrame({'label': all_labels})
                    label_counts = labels_df['label'].value_counts().head(20)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Top labels
                        fig_labels = px.bar(
                            x=label_counts.values,
                            y=label_counts.index,
                            orientation='h',
                            title="Top 20 Labels Mais Usadas"
                        )
                        fig_labels.update_layout(yaxis={'categoryorder': 'total ascending'})
                        st.plotly_chart(fig_labels, use_container_width=True)
                    
                    with col2:
                        # Distribuição de quantidade de labels por issue
                        fig_label_dist = px.histogram(
                            data,
                            x='labels_count',
                            title="Distribuição: Número de Labels por Issue",
                            labels={'labels_count': 'Número de Labels', 'count': 'Frequência'}
                        )
                        st.plotly_chart(fig_label_dist, use_container_width=True)
                    
                    # Tabela de labels
                    st.write("📊 **Estatísticas de Labels**")
                    st.dataframe(
                        pd.DataFrame({
                            'Label': label_counts.index,
                            'Quantidade': label_counts.values,
                            'Percentual': (label_counts.values / len(data) * 100).round(2)
                        }),
                        use_container_width=True
                    )
                else:
                    st.info("Nenhuma label encontrada nos dados.")
            
            with tab5:
                st.subheader("⏰ Análise Temporal")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Distribuição por hora do dia
                    hourly_dist = data['created_hour'].value_counts().sort_index()
                    fig_hours = px.bar(
                        x=hourly_dist.index,
                        y=hourly_dist.values,
                        title="Issues Criadas por Hora do Dia",
                        labels={'x': 'Hora', 'y': 'Número de Issues'}
                    )
                    st.plotly_chart(fig_hours, use_container_width=True)
                
                with col2:
                    # Distribuição por dia da semana
                    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    weekday_dist = data['created_weekday'].value_counts().reindex(weekday_order)
                    
                    fig_weekdays = px.bar(
                        x=['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
                        y=weekday_dist.values,
                        title="Issues Criadas por Dia da Semana",
                        labels={'x': 'Dia da Semana', 'y': 'Número de Issues'}
                    )
                    st.plotly_chart(fig_weekdays, use_container_width=True)
                
                # Heatmap de atividade
                st.subheader("🔥 Mapa de Calor de Atividade")
                
                # Criar dados para heatmap
                data['weekday_num'] = data['created_at'].dt.dayofweek
                heatmap_data = data.groupby(['weekday_num', 'created_hour']).size().reset_index()
                heatmap_data.columns = ['Dia', 'Hora', 'Issues']
                
                # Criar matriz para o heatmap
                heatmap_matrix = heatmap_data.pivot(index='Dia', columns='Hora', values='Issues').fillna(0)
                
                fig_heatmap = px.imshow(
                    heatmap_matrix,
                    labels=dict(x="Hora do Dia", y="Dia da Semana", color="Issues"),
                    y=['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
                    title="Mapa de Calor: Atividade por Dia e Hora"
                )
                st.plotly_chart(fig_heatmap, use_container_width=True)
        
        else:
            st.error("❌ Não foi possível carregar os dados. Verifique se o arquivo existe e está no formato correto.")
    
    else:
        # Tela de boas-vindas
        st.markdown("""
        ## 👋 Bem-vindo ao GitLab Issues Dashboard!
        
        Este dashboard permite visualizar e analisar issues extraídas do GitLab de forma interativa.
        
        ### 🚀 Para começar:
        
        1. **Configure uma extração** no painel lateral
        2. **Execute a extração** para coletar dados do GitLab
        3. **Explore os dados** nas diferentes abas do dashboard
        
        ### 📊 Funcionalidades disponíveis:
        
        - **Métricas em tempo real** sobre suas issues
        - **Gráficos interativos** para análise visual
        - **Filtros avançados** para explorar os dados
        - **Análises temporais** para identificar padrões
        - **Exportação de dados** em formato CSV
        
        ### 💡 Dicas:
        
        - Use **filtros por labels** para focar em tipos específicos de issues
        - **Extrações sem comentários** são mais rápidas
        - Mantenha o **número de páginas baixo** para testes iniciais
        
        ---
        
        👈 **Use o painel lateral para configurar e executar sua primeira extração!**
        """)

if __name__ == "__main__":
    main()