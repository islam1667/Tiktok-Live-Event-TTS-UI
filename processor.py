from queue import Queue
import time, threading
import TTS, UI
from multiprocessing import Queue
import time

sentences = Queue()
toggle = Queue()
thread = threading.Thread(target=UI.startUI, args=(toggle, ))
thread.start()

def add(text):
    sentences.put(text)

def loop():
    print("LOOP STARTED")
    while True:
        time.sleep(0.01)
        if not sentences.empty():
            toggle.put(1)
            TTS.talk(sentences.get())
            toggle.put(2)
            
def start():
    worker_thread = threading.Thread(target=loop)
    worker_thread.start()