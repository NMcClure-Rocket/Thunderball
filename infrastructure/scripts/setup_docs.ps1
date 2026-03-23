# setup_docs.ps1
# Installs MkDocs dependencies and builds the documentation site.
# Run from the repository root:  .\infrastructure\scripts\setup_docs.ps1

$ErrorActionPreference = 'Stop'

$repoRoot = Resolve-Path "$PSScriptRoot\..\.."

Write-Host "==> Installing MkDocs dependencies..."
py -m pip install mkdocs-material mkdocs-glightbox

Write-Host "==> Building documentation..."
py -m mkdocs build -f "$repoRoot\mkdocs.yml"

Write-Host "==> Done. Static site written to $repoRoot\site\"
Write-Host "    To serve locally, run: py -m mkdocs serve -f mkdocs.yml --dev-addr 127.0.0.1:8001"
