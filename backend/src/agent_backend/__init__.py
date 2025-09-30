"""AI Agent Backend Package."""

def main() -> None:
    """Entry point for the application."""
    from agent_backend.core import main as server_main
    server_main()
