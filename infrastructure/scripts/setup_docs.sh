#!/usr/bin/env bash
# setup_docs.sh
# Installs MkDocs dependencies and builds the documentation site.
# Run from the repository root:  bash infrastructure/scripts/setup_docs.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

echo "==> Installing MkDocs dependencies..."
pip install mkdocs-material mkdocs-glightbox

echo "==> Building documentation..."
python -m mkdocs build -f "$REPO_ROOT/mkdocs.yml"

echo "==> Done. Static site written to $REPO_ROOT/site/"
echo "    To serve locally, run: python -m mkdocs serve -f mkdocs.yml --dev-addr 127.0.0.1:8001"
