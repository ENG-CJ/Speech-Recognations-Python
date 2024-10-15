from system import shutdown
import pyttsx3 as tts
def confirm_action():
    shutdown()

def initConfirm():
    t = tts.init()
    t.say("Do you really  want to shutdown your computer yes or no?")
    t.runAndWait()
    


    
    