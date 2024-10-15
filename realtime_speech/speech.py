import speech_recognition as sr
import pyttsx3 as tts
from intents.greetings import greeting as detect_greeting
from intents.system import detect_system_command
from actions.greet import greet
from actions.system import shutdown, restart,execute_pending_action,request_confirmation
from intents.confirm import detect_confirmation
from actions.tasks import add_todo
from intents.tasks import task_matched
from actions.tasks import delete_todo_list,execute_todo_delete_confirmation,get_todo
engine=tts.init();
recognizer= sr.Recognizer();
pending_confirmation = False
todo_confirmation = False
task_adding=False

def speak_as_ai(text):
    print("")
    print("AI SPEAKING....")
    engine.say(text)
    engine.runAndWait()
    engine.stop();
def handle_intent(text):
    """Handles detected intents by executing corresponding actions."""
    global pending_confirmation,todo_confirmation,task_adding
   
    # for todo list
    
    if todo_confirmation:
        confirmation = detect_confirmation(text)
        if confirmation == "yes":
                execute_todo_delete_confirmation()
                todo_confirmation = False
        elif confirmation == "no":
                speak_as_ai("Todo deletion canceled.")
                todo_confirmation = False
        else:
                speak_as_ai("Please confirm by saying yes or no.")
                return

    

    if pending_confirmation:
        confirmation = detect_confirmation(text)
        if confirmation == "yes":
                execute_pending_action()
                pending_confirmation = False
        elif confirmation == "no":
                speak_as_ai("Action canceled.")
                pending_confirmation = False
        else:
                speak_as_ai("Please confirm by saying yes or no.")
                return

    if task_adding:
        todo_added=add_todo({"todo": text})
        print("The todo is ",todo_added)
        speak_as_ai("Added The Todo List Titled By "+text + " You can fetch now")
        task_adding=False
      
    
    if detect_greeting(text):
        greet()

    task_id = task_matched(text=text)
    if task_id in ["delete_todo"]:
        request_confirmation("delete this todo list")
        todo_confirmation=True
    if task_id in ["create_todo"]:
        speak_as_ai("Please Tell The Todo Name or the title to be stored")
        task_adding=True

    if task_id in ["fetch_todo"]:
        speak_as_ai("Now You Can see the todos in the terminal")
        print(get_todo())

        
    system_command = detect_system_command(text)
    if system_command == "shutdown":
        pending_confirmation=True
        request_confirmation("shutdown")
    elif system_command == "restart":
        pending_confirmation=True
        request_confirmation("restart")


def recognize_text():
   
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening")

        audio = recognizer.listen(source=source);

        transcribed= recognizer.recognize_google(audio)

        return transcribed

def is_terminate(text,data):
    token =text.split();
    for t in token:
        if t in data:
            return True
    return False


def listen_source():

    while True:
        q =["q","quit","exit"]
        text =recognize_text();
        print("You Said: ->",text)
        
        if is_terminate(text,q):
            break
        handle_intent(text)


listen_source()






