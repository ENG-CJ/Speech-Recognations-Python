TASKS = {
    "create_todo": [
        "create my todo list today",
        "create today list",
        "start a new todo list",
        "make a todo list",
        "add my task",
        "add my work"
    ],
    "fetch_todo": [
        "get my data",
        "fetch todo list",
        "get my todo list",
        "retrieve todo list"
    ],
    "read_todo": [
        "read my todo list",
        "show my todo list",
        "display my todo list"
    ],
    "delete_todo": [
        "delete my todo list",
        "delete todo list",
        "delete to-do list",
        "remove todo list",
        "clear todo list",
        "remove work"
    ],
    "update_todo": [
        "update todo list",
        "modify todo list",
        "edit my todo list",
        "update"
    ]
}


def task_matched(text):
    for task, variations in TASKS.items():
        for variation in variations:
            if variation.lower() in text.lower():  # Case-insensitive match
                print(f"Matched Task: {task}")
                return task
    return None
