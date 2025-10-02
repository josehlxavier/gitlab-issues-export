# GitLab Issues Extractor

Este projeto contém scripts para extrair informações de issues de projetos do GitLab usando a API pública.

## 🚀 Como usar

### Script Unificado (Recomendado)

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
