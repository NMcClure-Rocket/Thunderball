"""
Pytest configuration for backend tests.
Adds the backend directory to sys.path so that `from api.xxx import ...` works.
Also adds the repo root so that `from backend.xxx import ...` works for DAO modules.
"""
import sys
import os

_tests_backend_dir = os.path.dirname(os.path.abspath(__file__))
_repo_root = os.path.abspath(os.path.join(_tests_backend_dir, "..", ".."))
_backend_dir = os.path.join(_repo_root, "backend")

for _p in (_backend_dir, _repo_root):
    if _p not in sys.path:
        sys.path.insert(0, _p)
