"""
Health Check API
"""

from agent_backend.core import app

# Example route that will be auto-discovered
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "agent-backend"}