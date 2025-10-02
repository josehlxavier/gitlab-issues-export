#!/bin/bash
# Script para iniciar o Dashboard do GitLab Issues Extractor

echo "🚀 Iniciando GitLab Issues Dashboard..."

# Verificar se o Streamlit está instalado
if ! python -c "import streamlit" 2>/dev/null; then
    echo "📦 Instalando dependências..."
    pip install -r requirements.txt
fi

# Verificar se há dados de exemplo
if [ ! -d "reports" ] || [ -z "$(find reports -name '*.json' 2>/dev/null)" ]; then
    echo "📊 Não foram encontrados dados existentes."
    echo "💡 O dashboard irá permitir que você execute uma extração diretamente da interface."
fi

echo "🌐 Abrindo dashboard no navegador..."
echo "📍 URL: http://localhost:8501"
echo ""
echo "⚠️  Para parar o servidor, pressione Ctrl+C"
echo ""

# Iniciar o Streamlit
streamlit run streamlit_dashboard.py