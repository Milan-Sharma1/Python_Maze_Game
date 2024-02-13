from tkinter import *
from tkvideo import tkvideo
import pygame
pygame.mixer.init()
class Loading: #Loading window
    def __init__(self): #Create loading window
        self.load_window=Tk()
        self.load_window.geometry("300x100+560+300")
        self.load_window.title("Loading....")
        self.load_window.resizable(False,False)
        self.videoPlayer = Label(self.load_window)
        self.videoPlayer.pack()
        self.video = tkvideo("loading.mp4", self.videoPlayer ,size=(300,100))
        self.video.play()
        pygame.mixer.music.load("loading_music.wav")
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()
        self.load_window.after(4500, self.close_window)
    
    def close_window(self): #Close window
        self.load_window.destroy()


    def Load_loop(self): #Load the laoding loop
        self.load_window.focus_force()
        self.load_window.mainloop()
        