import threading
from collections import defaultdict


#key: text  value: function
#better be initialized before showing the dialogue
registered_func = defaultdict(list)

def thread(func):

    def wrapper(*args):
        # Do something before the function.
        x = threading.Thread(target= func, args=[*args])
        x.start()
        # Do something after the function.
    return wrapper

def register(text, func):
    registered_func[text] = func

    
def find_func(text):
    return registered_func[text]
   