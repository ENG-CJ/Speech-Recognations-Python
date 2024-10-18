import speech_recognition as sr
import pyttsx3 as tts
from intents.greetings import greeting as detect_greeting
from intents.system import detect_system_command
from actions.greet import greet
from actions.system import shutdown, restart,execute_pending_action,request_confirmation
from intents.confirm import detect_confirmation
from actions.tasks import add_todo
from intents.tasks import task_matched
from actions.tasks import *
from machine_intents.machine import *
engine=tts.init();
recognizer= sr.Recognizer();
pending_confirmation = False
todo_confirmation = False
task_adding=False
is_provided_id=False
is_updating=False
_is_providing_title=False
data={}
def speak_as_ai(text):
    print("")
    print("AI SPEAKING....")
    engine.say(text)
    engine.runAndWait()
    engine.stop();
def handle_intent(text):
    """Handles detected intents by executing corresponding actions."""
    global pending_confirmation,todo_confirmation,task_adding,is_provided_id,is_updating,_is_providing_title,data
    # custom machine learning intents
   
    # for todo list
    if _is_providing_title:
        data['title'] = text
        print("data updating ",data)
        data =update_todo(data=data)
        speak_as_ai(data)
        is_updating = False
        _is_providing_title=False
        data={}
        return
    if is_updating:
        _id = text
        data["id"]=_id;
        speak_as_ai("Provide updated title")
        _is_providing_title=True
        return

        
        

    if is_provided_id:
         data =execute_todo_delete_confirmation(todo_id=text)
         speak_as_ai(data)
         todo_confirmation = False
         is_provided_id = False
         return
    
    if todo_confirmation:
        confirmation = detect_confirmation(text)
        if confirmation == "yes":
                speak_as_ai("Please Provide The ID you want to delete")
                is_provided_id=True     
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
        response_todo=add_todo({"task": text})
        speak_as_ai(response_todo)
        task_adding=False
        return
      
    
    if detect_greeting(text):
        greet()
        return

    task_id = task_matched(text=text)
    if task_id in ["delete_todo"]:
        request_confirmation("delete this todo list")
        todo_confirmation=True
        return
    elif task_id in ["create_todo"]:
        speak_as_ai("Please Tell me the Todo title to be stored")
        task_adding=True
        return
        

    elif task_id in ["update_todo"]:
        speak_as_ai("Provide the id you want to update")
        is_updating=True
        return

    elif task_id in ["fetch_todo"]:
        data =get_todo()
        speak_as_ai("Now You Can see the todos in the terminal")
        print(data)
        return

        
    system_command = detect_system_command(text)
    if system_command == "shutdown":
        pending_confirmation=True
        request_confirmation("shutdown")
        return
    elif system_command == "restart":
        pending_confirmation=True
        request_confirmation("restart")
        return

    response,intent = predict_intent(text=text)
    speak_as_ai(response)


def recognize_text():
   
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            recognizer.energy_threshold = 3000
            print("Listening")
            audio = recognizer.listen(source=source,timeout=6, phrase_time_limit=10);

            transcribed= recognizer.recognize_google(audio)

            return transcribed
    except sr.UnknownValueError:
        speak_as_ai("I dont understand, Please try again");
        return None
    except sr.RequestError:
        speak_as_ai("Something went wrong. Please try again")
        return None

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
        if text:
            print("You Said: ->",text)
            
            if is_terminate(text,q):
                break
            handle_intent(text)


listen_source()






