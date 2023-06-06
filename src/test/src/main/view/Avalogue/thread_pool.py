import threading
from queue import  PriorityQueue
import time


class DialogueThread():

      
    newest_thread = None
    thread_count = 0
    
    @classmethod
    def set_newest_thread(cls, thread):
        cls.newest_thread = thread

    

    def get_value(self):
        return self.thread

    def __init__(self, task): 
        DialogueThread.thread_count += 1
        self.task = task
        self.id = DialogueThread.thread_count
        self.locker = threading.Event() # this event if for pausing and resuming the current thread
        self.locker.set()
        
        
        self.thread = threading.Thread(target=self.task, args=[self.locker])
        self.thread.start()

    

        w = threading.Thread(target=self.watch, args=[self.thread])
        w.start()
        
        DialogueThread.set_newest_thread(self.thread)
        
       
    def watch(self, thread: threading.Thread):
        
        while thread.is_alive():
                
                # if a new thread has arrived while this thread was working
                if DialogueThread.newest_thread is not None and self.id != DialogueThread.thread_count: 
                    #pause this thread
                    self.locker.clear()
                    
                #if the new thread is finished working
                if DialogueThread.newest_thread is not None and not  DialogueThread.newest_thread.is_alive():
                    #resume this thread
                    self.locker.set()


    



def thread1(locker : threading.Event):
     count = 0
     
     while count < 10:
        locker.wait()

        print(f"thread 1 is working: {count} ")
        count += 1
        time.sleep(1)
     print("thread1 is finished")


def thread2(locker : threading.Event):
     count = 0
     while count < 5:
        locker.wait()
        print(f"thread 2 is working: {count} ")
        count += 1
        time.sleep(1)


def input_checker():
    while True:
        DialogueThread.dummy = int(input())
         
     
thread_1 = DialogueThread(thread1)

time.sleep(5)
thread_2 = DialogueThread(thread2)


