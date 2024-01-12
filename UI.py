import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import threading, time, cv2, queue

class VideoPlayer:
    def __init__(self, root, video_source):
        self.root = root
        self.video_source = video_source
        self.cap = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(root, highlightthickness=0)
        self.canvas.pack()

        self.play_video()

    def play_video(self):
        ret, frame = self.cap.read()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.config(width=self.photo.width(), height=self.photo.height(), border=0)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.root.after(33, self.play_video)
        else:
            self.cap.release()

#-----------------------------------
def create_gif_display(root, gif_path, q):
    gif_running = False  # Flag to track if the GIF is running or not

    def update_gif(index):
        nonlocal frames, label, update_id, gif_running
        frame = frames[index]
        index = (index + 1) % len(frames)
        label.configure(image=frame)
        if gif_running:
            update_id = root.after(100, update_gif, index)

    def start_gif():
        nonlocal gif_running
        if not gif_running:  # If GIF is not running, start it
            gif_running = True
            update_gif(0)

    def stop_gif():
        # print(q.get())
        nonlocal gif_running
        gif_running = False  # Update the flag to indicate GIF stopped
        root.after_cancel(update_id)
        label.configure(image=frames[0])

    gif = Image.open(gif_path)
    # gif = gif.resize((300,300))
    frames = [ImageTk.PhotoImage(img.copy()) for img in ImageSequence.Iterator(gif)]

    label = tk.Label(root, image=frames[0], border=0)
    label.pack()

    update_id = None  # To store the update ID

    return start_gif, stop_gif

def startUI(q):
    root = tk.Tk()
    root.attributes("-topmost", True)
    start_gif, stop_gif = create_gif_display(root, r"C:\Users\islam\Desktop\TTBot 2\gif2.gif", q)
    # print("STARTUI")
    video_path = r'C:\Users\islam\Desktop\TTBot 2\pb.mp4'
    player = VideoPlayer(root, video_path)
    # start_button = tk.Button(root, text="Start GIF", command=start_gif)
    # start_button.pack()
    # stop_button = tk.Button(root, text="Stop GIF", command=stop_gif)
    # stop_button.pack()
    
    def checker(): 
        while True:
            # print("running....")
            time.sleep(0.01)
            if not q.empty():
                res = q.get()
                if res == 1:
                    time.sleep(0.5)
                    start_gif()
                elif res == 2:
                    stop_gif()
                
    thr = threading.Thread(target=checker, daemon=True)
    thr.start()

    root.configure(bg='lightgreen', border=0)
    root.mainloop()

if __name__ == '__main__':
    q = queue.Queue()
    thread = threading.Thread(target=startUI, args=(q,))
    thread.start()