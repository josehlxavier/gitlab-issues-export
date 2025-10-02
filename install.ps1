# Script de instalação das dependências do GitLab Issues Extractor para Windows
# Execute no PowerShell: .\install.ps1

Write-Host "🚀 Instalando dependências do GitLab Issues Extractor..." -ForegroundColor Green

# Verificar se o Python está instalado
try {
    $pythonVersion = python --version 2>$null
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python não encontrado. Por favor, instale o Python primeiro." -ForegroundColor Red
    Write-Host "   Download: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Verificar se o pip está instalado
try {
    $pipVersion = pip --version 2>$null
    Write-Host "✅ pip encontrado: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ pip não encontrado. Por favor, instale o pip primeiro." -ForegroundColor Red
    exit 1
}

# Atualizar pip
Write-Host "🔄 Atualizando pip..." -ForegroundColor Yellow
pip install --upgrade pip

# Instalar dependências
Write-Host "📚 Instalando dependências do requirements.txt..." -ForegroundColor Yellow
pip install -r requirements.txt

# Verificar instalação
Write-Host "✅ Verificando instalação..." -ForegroundColor Yellow
try {
    python -c "
import requests
import bs4
import lxml
print('✅ Todas as dependências foram instaladas com sucesso!')
print('📋 Versões instaladas:')
print(f'  • requests: {requests.__version__}')
print(f'  • beautifulsoup4: {bs4.__version__}')
print(f'  • lxml: {lxml.__version__}')
"
    
    Write-Host ""
    Write-Host "🎉 Instalação concluída!" -ForegroundColor Green
    Write-Host "💡 Para testar o script, execute:" -ForegroundColor Yellow
    Write-Host "   python gitlab_extractor_unified.py --help" -ForegroundColor Cyan
    
} catch {
    Write-Host "❌ Erro durante a verificação. Algumas dependências podem não ter sido instaladas corretamente." -ForegroundColor Red
}