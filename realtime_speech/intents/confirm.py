def detect_confirmation(text):
    """Detect 'yes' or 'no' confirmation from user input."""
    if "yes" in text.lower():
        return "yes"
    elif "no" in text.lower():
        return "no"
    return None
