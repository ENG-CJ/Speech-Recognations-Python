import pyttsx3

def greet():
    """Action to greet the user."""
    engine = pyttsx3.init()
    engine.say("Hello! How can I assist you today?")
    engine.runAndWait()
