#!/bin/bash
# Script para iniciar o Dashboard do GitLab Issues Extractor

echo "🚀 Iniciando GitLab Issues Dashboard..."

# Verificar se as dependências estão instaladas
echo "🔍 Verificando dependências..."

if ! python -c "import streamlit" 2>/dev/null; then
    echo "❌ Streamlit não encontrado. Instalando dependências..."
    pip install -r requirements.txt
fi

# Verificar se o script extrator existe
if [ ! -f "gitlab_extractor_unified.py" ]; then
    echo "❌ Script extrator não encontrado (gitlab_extractor_unified.py)"
    exit 1
fi

# Criar diretórios necessários se não existirem
mkdir -p reports/{json,csv,markdown,summary}

echo "✅ Ambiente configurado!"
echo "🌐 Iniciando dashboard em http://localhost:8501"
echo ""
echo "💡 Dicas de uso:"
echo "   • Use a barra lateral para configurar a extração"
echo "   • Clique em 'Extrair Issues' para buscar dados do GitLab"
echo "   • Explore as diferentes abas para análises detalhadas"
echo ""

# Iniciar o Streamlit
streamlit run dashboard.py