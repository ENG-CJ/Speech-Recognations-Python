import requests as req

URL ="http://localhost:4300/"

def add_todo_request(todo_data):
    print(todo_data)
    response = req.post(URL,json=todo_data)
    response=response.json()
    if(response["status"]):
        return f"The Todo Titled {todo_data['task']} Has been created"
    return "error occurred while creating the Todo"


def get_todo_list():
    response = req.get(URL)
    response=response.json()
    if(response["status"]):
        return response["data"]
    return "error occurred while fetching the Todo"

def delete_todo(id):
    response = req.delete(URL+"/"+str(id))
    response=response.json()
    print(response)
    if(response["status"]):
        return "Task that has an id "+str(id)+" Has been removed successfully"
    return "error occurred while fetching the Todo"

def update_todo(data):
    response = req.post(URL+"/update",json=data)
    response=response.json()
    print(response)
    if(response["status"]):
        return "Task that has an id "+str(data["id"])+" Has been updated successfully"
    return "error occurred while updating the Todo"

