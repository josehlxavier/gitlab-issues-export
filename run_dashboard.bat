@echo off
:: Script para iniciar o Dashboard do GitLab Issues Extractor no Windows

echo 🚀 Iniciando GitLab Issues Dashboard...

:: Verificar se Python está disponível
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado. Por favor, instale o Python primeiro.
    pause
    exit /b 1
)

:: Verificar se as dependências estão instaladas
echo 🔍 Verificando dependências...

python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo ❌ Streamlit não encontrado. Instalando dependências...
    pip install -r requirements.txt
)

:: Verificar se o script extrator existe
if not exist "gitlab_extractor_unified.py" (
    echo ❌ Script extrator não encontrado (gitlab_extractor_unified.py)
    pause
    exit /b 1
)

:: Criar diretórios necessários se não existirem
if not exist "reports" mkdir reports
if not exist "reports\json" mkdir reports\json
if not exist "reports\csv" mkdir reports\csv
if not exist "reports\markdown" mkdir reports\markdown
if not exist "reports\summary" mkdir reports\summary

echo ✅ Ambiente configurado!
echo 🌐 Iniciando dashboard em http://localhost:8501
echo.
echo 💡 Dicas de uso:
echo    • Use a barra lateral para configurar a extração
echo    • Clique em 'Extrair Issues' para buscar dados do GitLab
echo    • Explore as diferentes abas para análises detalhadas
echo.

:: Iniciar o Streamlit
streamlit run dashboard.py