import pyttsx3 as tts
from db.todo import TOODS
engine= tts.init()




def delete_todo_list(todo):
    engine.say("We will delete todo "+todo)
    engine.runAndWait()

def execute_todo_delete_confirmation(todo):
    engine.say("you deleted this todo named "+todo)
    engine.runAndWait()

def add_todo(todo):
    TOODS.append(todo)
    return TOODS

def get_todo():
    return TOODS
    


