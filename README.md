# GitLab Issues Extractor

Este projeto contém scripts para extrair informações de issues de projetos do GitLab usando a API pública.

## 🚀 Como usar

### 🎯 Dashboard Interativo (Recomendado)

Use o dashboard web interativo para extrair e visualizar dados:

```bash
# Iniciar o dashboard
streamlit run streamlit_dashboard.py

# Ou use os scripts de inicialização
./start_dashboard.sh      # Linux/macOS
start_dashboard.bat       # Windows
```

**Acesse:** http://localhost:8501

### Script de Linha de Comando

Use o script unificado `gitlab_extractor_unified.py` que combina todas as funcionalidades:

```bash
python gitlab_extractor_unified.py --help
```

### Extração básica

```bash
python gitlab_extractor_unified.py
```

### Scripts individuais (legacy)

Execute o script principal para extrair issues do projeto configurado:

```bash
python gitlab_api_extractor.py
```

Use o script configurável para mais opções:

```bash
python extract_gitlab_issues.py --help
```

#### Opções disponíveis do Script Unificado:

**Parâmetros Principais:**
- `--project`, `-p`: Caminho do projeto (formato: owner/repo)
- `--state`, `-s`: Estado das issues (`opened`, `closed`, `all`)
- `--pages`, `-n`: Número máximo de páginas a processar
- `--delay`, `-d`: Delay em segundos entre requests

**Filtros por Labels:**
- `--labels`: Labels específicas para filtro na API (separadas por vírgula)
- `--include-labels`: Incluir apenas issues com essas labels
- `--exclude-labels`: Excluir issues com essas labels

**Formatos de Saída:**
- `--output`, `-o`: Formatos de saída (`json`, `csv`, `markdown`, `summary`, `all`)
- `--filename`, `-f`: Nome personalizado para os arquivos (opcional)
- `--output-dir`: Diretório base para organizar os relatórios (default: `reports`)

**Controles:**
- `--include-comments`: Incluir comentários das issues
- `--no-comments`: Não buscar comentários das issues (mais rápido)
- `--verbose`, `-v`: Modo verboso

#### Exemplos:

```bash
# Extração básica com resumo e JSON
python gitlab_extractor_unified.py --output json,summary

# Extrair apenas issues com labels específicas em CSV
python gitlab_extractor_unified.py --include-labels "Bug,Enhancement" --output csv

# Filtrar issues excluindo certas labels com nome personalizado
python gitlab_extractor_unified.py --exclude-labels "wontfix,duplicate" --output all --filename "issues-filtradas"

# Extração completa com todos os formatos em diretório personalizado
python gitlab_extractor_unified.py --state all --pages 10 --output all --include-comments --output-dir "exports"

# Extração rápida focada apenas em bugs
python gitlab_extractor_unified.py --include-labels "Bug" --no-comments --output summary --filename "apenas-bugs"

# Usar filtro da API + filtro local com diretório específico
python gitlab_extractor_unified.py --labels "Bug,Enhancement" --exclude-labels "wontfix" --output-dir "bug-reports"
```

## 📁 Organização dos Arquivos

O script organiza automaticamente os arquivos em diretórios separados:

```
reports/ (ou diretório personalizado)
├── json/
│   └── gitlab-issues-2025-10-02.json
├── csv/
│   └── gitlab-issues-2025-10-02.csv
├── markdown/
│   └── gitlab-issues-2025-10-02.md
└── summary/
    └── gitlab-issues-2025-10-02.md
```

### Formatos de arquivo:

1. **JSON completo** (`json/`): Dados estruturados completos
2. **CSV** (`csv/`): Dados tabulares para análise em planilhas  
3. **Markdown detalhado** (`markdown/`): Relatório formatado com todas as informações
4. **Resumo** (`summary/`): Relatório resumido com estatísticas

### Nomenclatura padronizada:

- **Padrão**: `gitlab-issues-YYYY-MM-DD.extensão`
- **Personalizado**: `nome-personalizado-YYYY-MM-DD.extensão`

## 🏷️ Filtros por Labels

O script unificado oferece três tipos de filtros por labels:

### 1. Filtro da API (`--labels`)
- Aplicado diretamente na API do GitLab
- Mais eficiente para filtros simples
- Exemplo: `--labels "Bug,Enhancement"`

### 2. Filtro de Inclusão (`--include-labels`)
- Inclui apenas issues que contenham alguma das labels especificadas
- Aplicado após a busca da API
- Suporte a busca parcial (ex: "Bug" encontra "Critical Bug")
- Exemplo: `--include-labels "Bug,Critical"`

### 3. Filtro de Exclusão (`--exclude-labels`)
- Exclui issues que contenham alguma das labels especificadas
- Aplicado após a busca da API
- Suporte a busca parcial
- Exemplo: `--exclude-labels "wontfix,duplicate"`

### Combinando Filtros
```bash
# Usar filtro da API + filtros locais
python gitlab_extractor_unified.py \
  --labels "Bug" \
  --include-labels "Critical,High" \
  --exclude-labels "wontfix"
```

## 🎨 Dashboard Interativo

O projeto inclui um dashboard web completo construído com Streamlit que oferece:

### ✨ Funcionalidades do Dashboard:

- **🔍 Interface intuitiva** para configurar extrações
- **📊 Visualizações interativas** com gráficos dinâmicos
- **📈 Análises em tempo real** dos dados extraídos
- **🎯 Filtros avançados** por estado, autor, data e labels
- **📱 Design responsivo** que funciona em qualquer dispositivo
- **📥 Download de dados** filtrados em CSV

### 📊 Abas Disponíveis:

1. **Análises**: Gráficos e métricas principais
2. **Dados Brutos**: Tabela filtrada com todos os dados
3. **Autores**: Estatísticas e atividade por autor
4. **Labels**: Análise de tags e categorização
5. **Temporal**: Padrões de tempo e atividade

### 🎯 Como Usar o Dashboard:

1. Execute `streamlit run streamlit_dashboard.py`
2. Configure uma nova extração no painel lateral
3. Explore os dados nas diferentes abas
4. Use filtros para análises específicas
5. Baixe dados filtrados quando necessário

## 📂 Organização Automática de Arquivos

O script organiza automaticamente os relatórios em uma estrutura de diretórios clara:

### Estrutura Padrão:
```
reports/
├── json/        # Dados JSON estruturados
├── csv/         # Planilhas CSV
├── markdown/    # Relatórios detalhados
└── summary/     # Resumos executivos
```

### Vantagens da Organização:
- ✅ **Separação por tipo**: Cada formato em seu diretório
- ✅ **Nomenclatura consistente**: Padrão `gitlab-issues-YYYY-MM-DD`
- ✅ **Fácil localização**: Arquivos organizados por data
- ✅ **Personalização**: Nomes e diretórios customizáveis

### Exemplos de Organização:
```bash
# Diretório padrão "reports"
python gitlab_extractor_unified.py --output all

# Diretório personalizado
python gitlab_extractor_unified.py --output all --output-dir "exports"

# Nome personalizado + diretório específico
python gitlab_extractor_unified.py --output all --filename "bugs-criticos" --output-dir "bug-reports"
```

## 📊 Informações extraídas

Para cada issue, o script extrai:

### Dados básicos:
- ID e número da issue
- Título e descrição
- Autor e responsáveis
- Estado (aberta/fechada)
- Datas de criação, atualização e fechamento
- Labels e milestone
- URL da issue

### Métricas:
- Número de comentários
- Votos positivos/negativos
- Merge requests relacionados
- Estatísticas de tempo

### Comentários (se disponíveis):
- Conteúdo dos comentários
- Autor de cada comentário
- Datas dos comentários

## 🔧 Instalação

### Método Rápido (Recomendado)

```bash
# Instalar dependências
pip install -r requirements.txt

# Testar instalação
python gitlab_extractor_unified.py --help
```

### Scripts de Instalação Automática

**Linux/macOS:**
```bash
chmod +x install.sh
./install.sh
```

**Windows (PowerShell):**
```powershell
.\install.ps1
```

### Instalação Manual

```bash
pip install requests>=2.31.0 beautifulsoup4>=4.12.0 lxml>=4.9.0
```

### Para Desenvolvedores

```bash
pip install -r requirements-dev.txt
```

## 🎯 Dashboard Interativo

O projeto inclui um dashboard web interativo construído com Streamlit para visualização e análise dos dados extraídos.

### 🚀 Iniciar o Dashboard

**Método mais fácil:**

```bash
# Linux/macOS
./run_dashboard.sh

# Windows
run_dashboard.bat
```

**Método manual:**

```bash
streamlit run dashboard.py
```

### 📊 Funcionalidades do Dashboard

#### 🎛️ **Barra Lateral - Configurações**
- **Filtros Básicos**: Projeto, estado das issues, número de páginas
- **Filtros por Labels**: Incluir/excluir labels específicas
- **Configurações de Saída**: Formato e nome personalizado dos arquivos
- **Extração Integrada**: Botão para executar extração diretamente do dashboard

#### 📈 **Aba Dashboard**
- **Métricas Principais**: Total de issues, abertas, média de comentários, etc.
- **Gráfico de Pizza**: Distribuição por estado (abertas/fechadas)
- **Timeline**: Issues criadas nos últimos 30 dias
- **Top Autores**: 10 principais criadores de issues
- **Distribuição Horária**: Padrão de criação por hora do dia
- **Labels Mais Comuns**: Top 15 labels mais utilizadas

#### 📋 **Aba Dados Detalhados**
- **Filtros Avançados**: Por estado, autor e busca textual
- **Tabela Interativa**: Visualização completa dos dados
- **Download**: Exportar dados filtrados em CSV ou JSON
- **Estatísticas**: Contadores dinâmicos dos filtros aplicados

#### 📊 **Aba Análises**
- **Análise Temporal**: Distribuição por dia da semana
- **Análise de Comentários**: Categorização por quantidade
- **Matriz de Correlação**: Relação entre variáveis numéricas
- **Top Issues**: Por comentários e votos

#### 📁 **Aba Arquivos**
- **Gerenciamento**: Listar todos os arquivos gerados
- **Download Individual**: Baixar qualquer arquivo específico
- **Informações**: Tamanho e data de cada arquivo

### 🌐 **Acesso ao Dashboard**

Após iniciar, acesse: **http://localhost:8501**

### 💡 **Fluxo de Uso Recomendado**

1. **Configure** os parâmetros na barra lateral
2. **Execute** a extração clicando em "🚀 Extrair Issues"
3. **Explore** os dados nas diferentes abas
4. **Analise** os gráficos e métricas
5. **Exporte** os dados filtrados conforme necessário

## ⚙️ Configuração

### Projeto padrão

O projeto padrão está configurado para:
- **Projeto:** `raidiam-conformance/open-finance/certification`
- **Estado:** `opened` (issues abertas)
- **Páginas:** máximo 5 páginas
- **Delay:** 1 segundo entre requests

### Limitações da API

- A API pública do GitLab tem limites de rate limiting
- Comentários podem exigir autenticação em projetos privados
- Alguns campos podem não estar disponíveis em projetos públicos

## 📝 Estrutura dos arquivos

### `gitlab_extractor_unified.py` ⭐
**Script principal unificado** que combina todas as funcionalidades:
- Extração via API do GitLab
- Filtros avançados por labels
- Múltiplos formatos de saída
- Configuração completa via parâmetros

### Scripts individuais (legacy):

### `gitlab_api_extractor.py`
Script com a classe `GitLabAPIExtractor` que faz toda a extração.

### `extract_gitlab_issues.py`  
Script configurável via linha de comando.

### `create_reports.py`
Gera relatórios adicionais a partir dos dados JSON extraídos.

### `app.py`
Script original (mantido para compatibilidade).

## 🔍 Exemplo de uso completo

```bash
# 1. Extrair issues com filtros específicos organizados
python gitlab_extractor_unified.py \
  --include-labels "Bug,Enhancement" \
  --exclude-labels "wontfix" \
  --output all \
  --verbose \
  --filename "issues-filtradas" \
  --output-dir "relatorios"

# 2. Extração focada apenas em bugs críticos com data no nome
python gitlab_extractor_unified.py \
  --include-labels "Bug" \
  --labels "Critical,High" \
  --output csv,summary \
  --no-comments \
  --filename "bugs-criticos"

# 3. Relatório completo com comentários em diretório específico
python gitlab_extractor_unified.py \
  --state all \
  --include-comments \
  --output all \
  --pages 10 \
  --output-dir "exports/completo"
```

## 🚨 Notas importantes

1. **Rate Limiting**: Use delays apropriados para não sobrecarregar a API
2. **Projetos Privados**: Alguns dados podem não estar disponíveis
3. **Autenticação**: Para acessar comentários, pode ser necessário token de API
4. **Tamanho**: Projetos grandes podem gerar arquivos muito grandes

## 📈 Análise dos dados

Os arquivos CSV gerados podem ser importados em:
- Excel ou Google Sheets
- Power BI ou Tableau
- Python/Pandas para análises estatísticas
- Ferramentas de BI

## 🤝 Contribuições

Caso deseje contribuir para melhorar o script, estes são pontos que precisamos cobrir:
1. Adicionar tratamento de erros mais robusto
2. Implementar autenticação via token
3. Adicionar mais formatos de exportação
4. Melhorar a documentação

---

**Desenvolvido para extrair issues do GitLab de forma eficiente e organizada.**
