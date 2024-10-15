import os
import pyttsx3

pending_action = None  # To track pending shutdown or restart actions

def request_confirmation(action):
    """Request confirmation before executing a system command."""
    global pending_action
    engine = pyttsx3.init()
    pending_action = action  # Store the action for confirmation
    engine.say(f"Are you sure you want to {action}? Please say yes or no.")
    engine.runAndWait()


def execute_pending_action():
    """Execute the pending shutdown or restart action."""
    global pending_action
    if pending_action == "shutdown":
        shutdown()
    elif pending_action == "restart":
        restart()
    pending_action = None  # Reset pending action after execution
def shutdown():
    """Action to shutdown the system."""
    engine = pyttsx3.init()
    engine.say("Shutting down the system.")
    engine.runAndWait()
    os.system("shutdown /s /t 1")

def restart():
    """Action to restart the system."""
    engine = pyttsx3.init()
    engine.say("Restarting the system.")
    engine.runAndWait()
    os.system("shutdown /r /t 1")
