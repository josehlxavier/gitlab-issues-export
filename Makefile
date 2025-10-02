# Makefile para GitLab Issues Extractor

.PHONY: help install install-dev test lint format clean run example

# Variáveis
PYTHON = python
PIP = pip
SCRIPT = gitlab_extractor_unified.py

# Ajuda
help:
	@echo "🚀 GitLab Issues Extractor - Comandos Disponíveis:"
	@echo ""
	@echo "📦 Instalação:"
	@echo "  make install      - Instalar dependências de produção"
	@echo "  make install-dev  - Instalar dependências de desenvolvimento"
	@echo ""
	@echo "🔧 Desenvolvimento:"
	@echo "  make test         - Executar testes"
	@echo "  make lint         - Executar linting (pylint + flake8)"
	@echo "  make format       - Formatar código com black"
	@echo "  make check        - Verificar tipos com mypy"
	@echo ""
	@echo "🏃 Execução:"
	@echo "  make run          - Executar script com configurações padrão"
	@echo "  make example      - Executar exemplo com filtros"
	@echo ""
	@echo "🧹 Limpeza:"
	@echo "  make clean        - Limpar arquivos temporários"

# Instalação
install:
	@echo "📦 Instalando dependências de produção..."
	$(PIP) install -r requirements.txt

install-dev:
	@echo "📦 Instalando dependências de desenvolvimento..."
	$(PIP) install -r requirements-dev.txt

# Desenvolvimento
test:
	@echo "🧪 Executando testes..."
	pytest tests/ -v --cov=$(SCRIPT) --cov-report=html

lint:
	@echo "🔍 Executando linting..."
	pylint $(SCRIPT)
	flake8 $(SCRIPT)

format:
	@echo "✨ Formatando código..."
	black $(SCRIPT)

check:
	@echo "🔎 Verificando tipos..."
	mypy $(SCRIPT)

# Execução
run:
	@echo "🏃 Executando script padrão..."
	$(PYTHON) $(SCRIPT) --output summary --no-comments --pages 1

example:
	@echo "🏃 Executando exemplo com filtros..."
	$(PYTHON) $(SCRIPT) \
		--include-labels "Bug" \
		--output csv,summary \
		--no-comments \
		--filename "exemplo" \
		--verbose

# Limpeza
clean:
	@echo "🧹 Limpando arquivos temporários..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Limpeza concluída!"

# Instalação completa
setup: install-dev
	@echo "🎉 Ambiente de desenvolvimento configurado!"
	@echo "💡 Execute 'make help' para ver os comandos disponíveis"