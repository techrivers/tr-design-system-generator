"""Vercel serverless function entry point for FastAPI app."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from web.app import app

# Vercel Python runtime expects the ASGI app directly
# The @vercel/python builder will handle the ASGI conversion
