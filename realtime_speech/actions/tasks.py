import pyttsx3 as tts
from db.todo import TOODS
from requests_actions.task_request import *
engine= tts.init()




def delete_todo_list(todo):
    engine.say("We will delete todo "+todo)
    engine.runAndWait()

def execute_todo_delete_confirmation(todo_id):
    response = delete_todo(todo_id)
    return response

def exec_update(data):
    response = update_todo(data=data)
    return response

def add_todo(todo):
  response =add_todo_request(todo)
  return response

def get_todo():
    response = get_todo_list()
    return response
    


