# 🎯 GitLab Issues Extractor - Guia de Uso Completo

## 📋 Visão Geral

Este projeto oferece uma solução completa para extrair, organizar e visualizar issues do GitLab, incluindo:
- 🔧 Extração automatizada via API do GitLab
- 📊 Dashboard interativo para análise de dados
- 📁 Organização estruturada de arquivos
- 📈 Visualizações e relatórios avançados

## 🚀 Início Rápido

### 1. Instalação
```bash
pip install -r requirements.txt
```

### 2. Dashboard Interativo
```bash
# Método mais fácil
./run_dashboard.sh    # Linux/macOS
run_dashboard.bat     # Windows

# Ou manualmente
streamlit run dashboard.py
```

Acesse: **http://localhost:8501**

### 3. Extração via Linha de Comando
```bash
python gitlab_extractor_unified.py --project-id 123456 --project-name "meu-projeto"
```

## 📊 Funcionalidades do Dashboard

### 🎛️ Configurações (Barra Lateral)
- **Projeto**: ID e nome do projeto GitLab
- **Filtros**: Estado das issues, número de páginas
- **Labels**: Incluir/excluir labels específicas
- **Formato**: JSON, CSV ou ambos
- **Extração**: Botão integrado para executar

### 📈 Abas Disponíveis

#### 1. **Dashboard Principal**
- Métricas principais (total, abertas, comentários)
- Gráfico de distribuição por estado
- Timeline dos últimos 30 dias
- Top 10 autores mais ativos
- Distribuição horária de criação
- Labels mais utilizadas

#### 2. **Dados Detalhados**
- Tabela interativa com todos os dados
- Filtros por estado, autor e busca textual
- Download dos dados filtrados
- Estatísticas dinâmicas

#### 3. **Análises Avançadas**
- Distribuição por dia da semana
- Análise de comentários por categoria
- Matriz de correlação entre variáveis
- Top issues por comentários e votos

#### 4. **Gerenciamento de Arquivos**
- Lista de todos os arquivos gerados
- Download individual de qualquer arquivo
- Informações de tamanho e data

## 🔧 Extração via CLI

### Uso Básico
```bash
python gitlab_extractor_unified.py \
  --project-id 123456 \
  --project-name "meu-projeto"
```

### Opções Avançadas
```bash
python gitlab_extractor_unified.py \
  --project-id 123456 \
  --project-name "meu-projeto" \
  --include-labels "bug,feature" \
  --exclude-labels "wontfix,duplicate" \
  --state "opened" \
  --pages 5 \
  --format "both" \
  --output-name "relatorio_custom"
```

### Parâmetros Disponíveis

| Parâmetro | Descrição | Exemplo |
|-----------|-----------|---------|
| `--project-id` | ID do projeto GitLab | `123456` |
| `--project-name` | Nome do projeto | `"meu-projeto"` |
| `--include-labels` | Labels a incluir | `"bug,feature"` |
| `--exclude-labels` | Labels a excluir | `"wontfix"` |
| `--state` | Estado das issues | `opened/closed/all` |
| `--pages` | Número de páginas | `5` |
| `--format` | Formato de saída | `json/csv/both` |
| `--output-name` | Nome personalizado | `"relatorio"` |

## 📁 Estrutura de Arquivos Gerada

```
reports/
├── json/           # Arquivos JSON
│   └── issues_projeto_20241002_1845.json
├── csv/            # Arquivos CSV
│   └── issues_projeto_20241002_1845.csv
└── combined/       # Quando formato="both"
    ├── issues_projeto_20241002_1845.json
    └── issues_projeto_20241002_1845.csv
```

## 🎯 Casos de Uso

### 1. **Análise de Produtividade**
- Visualizar issues criadas por período
- Identificar autores mais ativos
- Analisar padrões de horário

### 2. **Gestão de Labels**
- Identificar labels mais utilizadas
- Filtrar por categorias específicas
- Análise de distribuição

### 3. **Relatórios Executivos**
- Métricas principais em tempo real
- Exportação de dados filtrados
- Visualizações prontas para apresentação

### 4. **Auditoria e Compliance**
- Histórico completo de issues
- Rastreabilidade por autor
- Dados estruturados para análise

## 🔍 Exemplos Práticos

### Extrair apenas bugs abertos
```bash
python gitlab_extractor_unified.py \
  --project-id 123456 \
  --project-name "meu-projeto" \
  --include-labels "bug" \
  --state "opened"
```

### Relatório completo excluindo duplicatas
```bash
python gitlab_extractor_unified.py \
  --project-id 123456 \
  --project-name "meu-projeto" \
  --exclude-labels "duplicate,wontfix" \
  --format "both" \
  --pages 10
```

### Análise de features implementadas
```bash
python gitlab_extractor_unified.py \
  --project-id 123456 \
  --project-name "meu-projeto" \
  --include-labels "feature" \
  --state "closed" \
  --output-name "features_implementadas"
```

## 🛠️ Solução de Problemas

### Dashboard não inicia
```bash
# Verificar instalação
pip install streamlit plotly pandas

# Executar com logs
streamlit run dashboard.py --logger.level debug
```

### Erro na extração
```bash
# Verificar conectividade
curl -I https://gitlab.com

# Verificar project-id
# Acesse: https://gitlab.com/seu-projeto → Settings → General
```

### Arquivos não encontrados
```bash
# Verificar diretório
ls -la reports/

# Recriar estrutura
mkdir -p reports/{json,csv,combined}
```

## 📈 Próximos Passos

1. **Configure** seu projeto no dashboard
2. **Execute** a primeira extração
3. **Explore** as visualizações disponíveis
4. **Exporte** os dados conforme necessário
5. **Automatize** extrações regulares

## 🆘 Suporte

Para problemas ou sugestões:
1. Verifique os logs no terminal
2. Confirme a conectividade com o GitLab
3. Valide o project-id e permissões
4. Consulte a documentação da API GitLab

---
**Desenvolvido com ❤️ para análise eficiente de projetos GitLab**