# Publicar Math Animator en GitHub + Streamlit Cloud
# Ejecutar en PowerShell desde esta carpeta.

$ErrorActionPreference = "Stop"
$Repo = "https://github.com/Kyloren1540/math-animator.git"

Write-Host "=== 1. Comprobar sesión de GitHub ===" -ForegroundColor Cyan
gh auth status
if ($LASTEXITCODE -ne 0) {
    Write-Host "Inicia sesión en el navegador (cuenta Kyloren1540):" -ForegroundColor Yellow
    gh auth login -h github.com -p https -w -s repo
}

Write-Host "`n=== 2. Crear repositorio (si no existe) y subir código ===" -ForegroundColor Cyan
git remote set-url origin $Repo
$exists = gh repo view Kyloren1540/math-animator 2>$null
if ($LASTEXITCODE -ne 0) {
    gh repo create Kyloren1540/math-animator --public --description "Math Animator - visualizador de funciones" --source=. --remote=origin --push
} else {
    git push -u origin main
}

Write-Host "`n=== 3. Listo en GitHub ===" -ForegroundColor Green
Write-Host "Repo: https://github.com/Kyloren1540/math-animator"
Write-Host ""
Write-Host "=== 4. Streamlit Cloud (manual, una vez) ===" -ForegroundColor Cyan
Write-Host "1. Abre https://share.streamlit.io"
Write-Host "2. New app -> repo Kyloren1540/math-animator"
Write-Host "3. Main file: streamlit_app.py -> Deploy"
Write-Host "Enlace: https://math-animator-kyloren1540.streamlit.app (o similar)"
