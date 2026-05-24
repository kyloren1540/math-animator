# Publicar Math Animator en GitHub + Streamlit Cloud
# Ejecutar en PowerShell desde esta carpeta.

$ErrorActionPreference = "Stop"
$RepoOwner = "Kyloren1540"
$RepoName = "math-animator"
$RepoUrl = "https://github.com/$RepoOwner/$RepoName.git"

Write-Host "=== 1. Comprobar sesión de GitHub ===" -ForegroundColor Cyan
gh auth status
if ($LASTEXITCODE -ne 0) {
    Write-Host "Inicia sesión en el navegador (cuenta Kyloren1540):" -ForegroundColor Yellow
    gh auth login -h github.com -p https -w -s repo
    if ($LASTEXITCODE -ne 0) { exit 1 }
}

Write-Host "`n=== 2. Crear repositorio (si no existe) y subir código ===" -ForegroundColor Cyan
git remote set-url origin $RepoUrl

$repoExists = $false
$prevErrorAction = $ErrorActionPreference
$ErrorActionPreference = "SilentlyContinue"
try {
    gh repo view "$RepoOwner/$RepoName" --json name -q .name 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) { $repoExists = $true }
} finally {
    $ErrorActionPreference = $prevErrorAction
}

if (-not $repoExists) {
    Write-Host "Creando repositorio $RepoOwner/$RepoName ..." -ForegroundColor Yellow
    gh repo create "$RepoOwner/$RepoName" --public `
        --description "Math Animator - visualizador de funciones"
    if ($LASTEXITCODE -ne 0) { exit 1 }
    git remote set-url origin $RepoUrl
    git push -u origin main
    if ($LASTEXITCODE -ne 0) { exit 1 }
} else {
    Write-Host "El repositorio ya existe. Subiendo cambios..." -ForegroundColor Yellow
    git push -u origin main
    if ($LASTEXITCODE -ne 0) { exit 1 }
}

Write-Host "`n=== 3. Listo en GitHub ===" -ForegroundColor Green
Write-Host "Repo: https://github.com/$RepoOwner/$RepoName"
Write-Host ""
Write-Host "=== 4. Streamlit Cloud (manual, una vez) ===" -ForegroundColor Cyan
Write-Host "1. Abre https://share.streamlit.io"
Write-Host "2. New app -> repo $RepoOwner/$RepoName"
Write-Host "3. Main file: streamlit_app.py -> Deploy"
