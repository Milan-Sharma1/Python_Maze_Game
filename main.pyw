from tkinter import *
from PIL import Image, ImageTk
import sys
import game 
import loading as loop
import pygame

pygame.mixer.init()

class New_Window: #Creating main starting window
    def __init__(self):
        self.window1 = Tk()
        self.window1.geometry("600x350+500+200")
        self.window1.title("Maze Runner")
        self.window1.resizable(False, False)

        self.canvas1 = Canvas(self.window1, height=350, width=600, bg="lightyellow", bd=0, relief="solid")
        self.canvas1.pack()

        self.image_start = Image.open("start_background.gif")
        self.photo_start = ImageTk.PhotoImage(image=self.image_start)
        self.canvas1.create_image(0, 0, anchor=NW, image=self.photo_start)
        self.start_audio()
        self.start_frame = Frame(self.canvas1, bg='white')
        self.start_frame.place(relx=0.5, rely=0.7, anchor='center')
        self.window1.protocol("WM_DELETE_WINDOW", exit)

    def start_audio(self):
        pygame.mixer.music.load("Title.mp3")
        pygame.mixer.music.set_volume(100)
        pygame.mixer.music.play()


    def Start(self): #Destroy the window function
        pygame.mixer.music.stop()
        self.window1.destroy()

    def exit(self): #Exit the game
        sys.exit()
    
    def create_buttons(self): #To create a buttons
        self.start_image = Image.open("start_button.gif")
        self.start_image = self.start_image.resize((100, 50))
        self.exit_image = Image.open("exit_button.gif")
        self.exit_image = self.exit_image.resize((100, 50))
        self.photo_exit_button = ImageTk.PhotoImage(self.exit_image)
        self.photo_start_button = ImageTk.PhotoImage(self.start_image)
        self.button_exit = Button(self.start_frame,image = self.photo_exit_button, command=self.exit) #Button to exit
        self.button_exit.pack(side="bottom")
        self.button_start = Button(self.start_frame, image=self.photo_start_button, command=self.Start) #Button to start
        self.button_start.pack(side="bottom")
    

    def Run_loop(self): #Run the Main window loop
        self.create_buttons()
        self.window1.mainloop()
        self.load = loop.Loading()
        self.load.Load_loop()
        self.game = game.MazeGame()
        self.game.mainloop()


if __name__ == "__main__": #Start the Main loop
    Main_win = New_Window()
    Main_win.Run_loop()

    