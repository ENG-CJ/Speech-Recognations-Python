def detect_system_command(text):
    """Detect system commands like shutdown or restart."""
    if "shutdown" in text.lower():
        return "shutdown"
    elif "restart" in text.lower():
        return "restart"
    return None
