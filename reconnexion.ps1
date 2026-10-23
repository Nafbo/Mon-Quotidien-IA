# Renouvelle la session NotebookLM et la copie dans le presse-papiers.
# Ensuite : coller la valeur dans NOTEBOOKLM_AUTH_JSON (environnement cloud
# sur claude.ai/code). Chaque reconnexion est notée dans reconnexions.log
# pour suivre leur fréquence.

$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

& .\.venv\Scripts\notebooklm.exe login --browser msedge
if ($LASTEXITCODE -ne 0) { throw "La connexion a échoué." }

$storage = Join-Path $HOME '.notebooklm\profiles\default\storage_state.json'
# Compacté sur une ligne : plus simple à coller dans le format .env
$json = Get-Content $storage -Raw | ConvertFrom-Json | ConvertTo-Json -Depth 20 -Compress
Set-Clipboard -Value "NOTEBOOKLM_AUTH_JSON='$json'"

$last = Get-Content reconnexions.log -ErrorAction SilentlyContinue | Select-Object -Last 1
$now = Get-Date
if ($last) {
    $days = [math]::Round(($now - [datetime]::Parse($last.Split(' ')[0])).TotalDays, 1)
    Write-Host "Dernière reconnexion il y a $days jours."
}
Add-Content reconnexions.log $now.ToString('s')

Write-Host "Session copiée. Collez-la à la place de la ligne NOTEBOOKLM_AUTH_JSON sur claude.ai/code."
