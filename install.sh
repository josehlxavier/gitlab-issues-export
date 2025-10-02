#!/bin/bash
# Script de instalação das dependências do GitLab Issues Extractor

echo "🚀 Instalando dependências do GitLab Issues Extractor..."

# Verificar se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale o Python 3 primeiro."
    exit 1
fi

# Verificar se o pip está instalado
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip não encontrado. Por favor, instale o pip primeiro."
    exit 1
fi

# Determinar qual comando pip usar
PIP_CMD="pip"
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
fi

echo "📦 Usando $PIP_CMD para instalação..."

# Atualizar pip
echo "🔄 Atualizando pip..."
$PIP_CMD install --upgrade pip

# Instalar dependências
echo "📚 Instalando dependências do requirements.txt..."
$PIP_CMD install -r requirements.txt

# Verificar instalação
echo "✅ Verificando instalação..."
python3 -c "
import requests
import bs4
import lxml
print('✅ Todas as dependências foram instaladas com sucesso!')
print('📋 Versões instaladas:')
print(f'  • requests: {requests.__version__}')
print(f'  • beautifulsoup4: {bs4.__version__}')
print(f'  • lxml: {lxml.__version__}')
"

echo ""
echo "🎉 Instalação concluída!"
echo "💡 Para testar o script, execute:"
echo "   python3 gitlab_extractor_unified.py --help"