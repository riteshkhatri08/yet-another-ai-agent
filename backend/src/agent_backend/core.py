"""
Core module that exports commonly used objects across the application.

This module serves as a central place to import and re-export
key objects like the FastAPI app instance and configuration settings.
"""

from .server import app, main
from .config import settings


__all__ = ["app", "main", "settings"]
