from tkinter import *
from random import *
from PIL import Image, ImageTk
import json
import loading as loop
import sys
import pygame

pygame.mixer.init()

class MazeGame:
    def __init__(self):
        # Create the game window
        self.window = Tk()
        self.window.geometry("780x790+350-30")
        self.window.title("The Maze")
        self.window.resizable(False,False)
        self.image = PhotoImage(file="background.gif", height=796, width= 796)
        self.image_label = Label(self.window, image=self.image)
        self.image_label.place(x=0,y=0)
        self.Main_frame = Frame(self.window, width=700,height=600, background="lightblue")
        self.Main_frame.place(x=50, y=100)
        self.canvas = Canvas(self.Main_frame, width=650, height=550, bg="lightyellow", bd=0, relief="solid")
        self.canvas.place(x=25,y=25)
        self.game_music()
        self.my_list = []
        self.main_list = []
        self.removed_line = []
        self.rcords = []
        self.unique_sorted_list = []
        
    def create_vertical_lines(self): #Selecting vertical line coordinates and storing in my_list
        x = randrange(0,650,25)
        x1 = randrange(0,550,25)
        x2 = x
        x3 = x1+25
        list1 = []
        list1.append(x)
        list1.append(x1)
        list1.append(x2)
        list1.append(x3)   
        self.main_list.append(list1)

    def create_horizontal_lines(self): #Selecting horizontal line coordinates and storing in my_list
        x = randrange(0,650,25)
        x1 = randrange(0,550,25)
        x2 = x+25
        x3 = x1
        list1 = []
        list1.append(x)
        list1.append(x1)
        list1.append(x2)
        list1.append(x3)
        self.main_list.append(list1)

    def make_maze(self): #Creating a Grid using all the vertical and horizontal line combination and storing all the unique sorted coordinates 
        i = 0
        while i<5000:
            self.create_vertical_lines()
            self.create_horizontal_lines()
            i+=1
        set_list = set(map(tuple, self.main_list))
        self.unique_sorted_list = list(map(list, set_list))
        self.unique_sorted_list.sort()

    def remover(self,rc): #Function to remove particular coordinate (line) from the grid
        self.unique_sorted_list.remove(rc)

    def random_remove(self): #removing random lines to create a maze
        j=0
        with open("paths.txt","r") as file:
            lines = file.readlines()
            line = choice(lines)
            xlist = json.loads(line)
            self.my_list.extend(xlist)
        for x in xlist:
            self.unique_sorted_list.remove(x)
            for xx in x:
                self.removed_line.append(xx)
        if self.removed_line[-4]==625 and self.removed_line[-2]==625: #creating a green box as the ending
            rect = self.canvas.create_rectangle(self.removed_line[-4],self.removed_line[-3],self.removed_line[-4]+25,self.removed_line[-3]+25, fill="green2", outline="red")
            r1,r2,r3,r4 = self.canvas.coords(rect)
            self.rcords.append(r1)
            self.rcords.append(r2)
            self.rcords.append(r3)
            self.rcords.append(r4)
        while j<400:
            rc=choice(self.unique_sorted_list)
            self.remover(rc)
            for i in range(4):
                x=rc[i]
                self.removed_line.append(x)
            j+=1

    def End_call(self): #function to excute after completing the maze
        self.window.withdraw()
        self.congrats = Toplevel(self.window)
        self.congrats.geometry("800x400")
        self.congrats.resizable(False,False)
        image3 = Image.open("Hooray.gif")
        image4 = image3.resize((800,500))
        create_image = ImageTk.PhotoImage(image4)
        label = Label(self.congrats, image=create_image)
        label.place(x=0,y=0)
        self.Clearing_audio()
        self.channel1.stop()
        self.channel2.stop()
        openimgbtn1 = Image.open("nextbtn1.gif")
        resizebtn1 = openimgbtn1.resize((100,40))
        createbtn1 = ImageTk.PhotoImage(resizebtn1)
        button1 = Button(self.congrats, image=createbtn1, command=self.reset) #Next level button
        button1.place(x=350, y=250)
        openimgbtn2 = Image.open("exit_button1.gif")
        resizebtn2 = openimgbtn2.resize((100,40))
        createbtn2 = ImageTk.PhotoImage(resizebtn2)
        button2 = Button(self.congrats, image=createbtn2, command=self.exit) #Exit button
        button2.place(x=350, y=300)
        self.congrats.protocol("WM_DELETE_WINDOW", self.do_nothing)
        self.congrats.mainloop()

    def exit(self): #Exit function
        sys.exit()

    def reset(self): #Reset the game window and restart it
        pygame.mixer.music.stop()
        self.window.destroy()
        self.load = loop.Loading()
        self.load.Load_loop()
        self.game = MazeGame()
        self.game.mainloop()

    def game_music(self):
        self.sound1 = pygame.mixer.Sound("gameplaymusic.mp3")
        self.channel1 = pygame.mixer.Channel(0)
        self.channel1.set_volume(100)
        self.channel1.play(self.sound1,loops = -1)


    def audio(self):
        self.sound2 = pygame.mixer.Sound("move-self.mp3")
        self.channel2 = pygame.mixer.Channel(1)
        self.channel2.set_volume(100)
        self.channel2.play(self.sound2)

    def Clearing_audio(self):
        pygame.mixer.music.load("True_ending.wav")
        pygame.mixer.music.set_volume(100)
        pygame.mixer.music.play()

    def move_left(self,event): #move the game object left
        cor=list(self.canvas.bbox(self.game_obj))
        temp=cor.copy()
        temp[0]-=2
        temp[2]-=22
        temp[3]+=5
        for i in range(0,len(self.removed_line),4):
            if temp[0]  == self.removed_line[i] and temp[1] == self.removed_line[i+1] and temp[2] == self.removed_line[i+2] and temp[3] == self.removed_line[i+3]:  
                if temp[0]==0:
                    return 0
                else:  
                    x = -25
                    y = 0
                    self.canvas.move(self.game_obj, x, y)
                    self.audio()
                    if temp[0]==self.rcords[0] and temp[1]==self.rcords[1]: #condition to check if the game object has reached end
                        self.End_call()
                    temp.clear()
                    return 0
            
    def move_right(self,event): #move the game object right
        cor=list(self.canvas.bbox(self.game_obj))
        temp=cor.copy()
        temp[0]-=2
        temp[0]+=25
        temp[2]+=3
        temp[3]+=5
        for i in range(0,len(self.removed_line),4):
            if temp[0]  == self.removed_line[i] and temp[1] == self.removed_line[i+1] and temp[2] == self.removed_line[i+2] and temp[3] == self.removed_line[i+3]:
                x = 25
                y = 0
                self.canvas.move(self.game_obj, x, y)
                self.audio()
                if temp[0]==self.rcords[0] and temp[1]==self.rcords[1]: #condition to check if the game object has reached end
                    self.End_call()
                temp.clear()
                return 0

    def move_up(self,event): #move the game object up
        cor=list(self.canvas.bbox(self.game_obj))
        temp=cor.copy()
        temp[0]-=2
        temp[2]+=3
        temp[3]-=20
        for i in range(0,len(self.removed_line),4):
            if temp[0]  == self.removed_line[i] and temp[1] == self.removed_line[i+1] and temp[2] == self.removed_line[i+2] and temp[3] == self.removed_line[i+3]:    
                if temp[1]==0:
                    return 0 
                else:
                    x = 0
                    y = -25
                    self.canvas.move(self.game_obj, x, y)
                    self.audio()
                    if temp[0]==self.rcords[0] and temp[1]==self.rcords[1]: #condition to check if the game object has reached end
                        self.End_call()
                    temp.clear()
                    return 0

    def move_down(self,event): #move the game object down
        cor=list(self.canvas.bbox(self.game_obj))
        temp=cor.copy()
        temp[0]-=2
        temp[1]+=25
        temp[2]+=3
        temp[3]+=5
        for i in range(0,len(self.removed_line),4):
            if temp[0]  == self.removed_line[i] and temp[1] == self.removed_line[i+1] and temp[2] == self.removed_line[i+2] and temp[3] == self.removed_line[i+3]:    
                x = 0
                y = 25
                self.canvas.move(self.game_obj, x, y)
                self.audio()
                if temp[0]==self.rcords[0] and temp[1]==self.rcords[1]: #condition to check if the game object has reached end
                    self.End_call()
                temp.clear()
                return 0
    
    def do_nothing(self): #to disable the closing function
        pass

    def Create_game_obj(self): #create a game object
        image1 = Image.open("gameobj.png")
        image2 = image1.resize((20,20))
        self.astrisk = ImageTk.PhotoImage(image2)
        self.game_obj = self.canvas.create_image(12, self.my_list[0][1] + 10, image=self.astrisk)

    def create_lines(self): #Apply all the remaining lines after removing random lines
        for a in self.unique_sorted_list:    
            self.canvas.create_line(a)

    def mainloop(self): #start the mainloop for this window
        self.make_maze()
        self.random_remove()
        self.Create_game_obj()
        self.create_lines()
        #Binding Keyboard keys for gameobj movement
        self.window.bind("<Left>", self.move_left)
        self.window.bind("<a>", self.move_left)
        self.window.bind("<Right>", self.move_right)
        self.window.bind("<d>", self.move_right)
        self.window.bind("<Up>", self.move_up)
        self.window.bind("<w>", self.move_up)
        self.window.bind("<Down>", self.move_down)
        self.window.bind("<s>", self.move_down)
        self.window.focus_force()
        self.window.mainloop()