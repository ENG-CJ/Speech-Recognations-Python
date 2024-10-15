greetings=["asc","asalamu alaykum","hi","hey","hello","hello there","yey"]
def greeting(text):
    for greet in greetings:
        if greet in text.lower():
            return True
    return False