@echo off
REM Script para iniciar o Dashboard do GitLab Issues Extractor no Windows

echo 🚀 Iniciando GitLab Issues Dashboard...

REM Verificar se o Streamlit está instalado
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo 📦 Instalando dependências...
    pip install -r requirements.txt
)

REM Verificar se há dados de exemplo
if not exist "reports" (
    echo 📊 Não foram encontrados dados existentes.
    echo 💡 O dashboard irá permitir que você execute uma extração diretamente da interface.
) else (
    dir /b reports\*.json >nul 2>&1
    if errorlevel 1 (
        echo 📊 Não foram encontrados dados existentes.
        echo 💡 O dashboard irá permitir que você execute uma extração diretamente da interface.
    )
)

echo 🌐 Abrindo dashboard no navegador...
echo 📍 URL: http://localhost:8501
echo.
echo ⚠️  Para parar o servidor, pressione Ctrl+C
echo.

REM Iniciar o Streamlit
streamlit run streamlit_dashboard.py