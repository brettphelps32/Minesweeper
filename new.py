import tkinter as tk
import customtkinter
from tkinter import *
import random
import math
from PIL import ImageTk, Image


customtkinter.set_ctk_parent_class(tk.Tk)

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue
mode = "dark"




class MainGUI:
    def __init__(self):
        self.root = customtkinter.CTk() 
        self.root.geometry("500x500")
        self.root.title("MineSweeper")

        #Slider Variables
        self.columnSize = DoubleVar()
        self.rowSize = DoubleVar()

        #Supporting Variables
        self.bombsPlaced = False
        self.btnList = [[]]
        self.visitedTile = []
        self.bombMarked = []




        self.startMenu()

    #Creates a menu to create the board
    def startMenu(self):
        #Frame creation
        self.buildingFrame = customtkinter.CTkFrame(self.root, width = 500, height= 500)
        self.buildingFrame.pack()

        # Supporting Functions
        def slidingCol(self):
            labelColumn.configure(text=int(sliderCol.get()))
        def slidingRow(self):
            labelRow.configure(text=int(sliderRow.get()))
        
        def changeMode():
            global mode
            if mode == "dark":
                customtkinter.set_appearance_mode("light")
                mode = "light"
            else:
                customtkinter.set_appearance_mode("dark")
                mode = "dark"

        # Column Selector and labels
        label = customtkinter.CTkLabel(self.buildingFrame, text="Select column size")
        label.place(relx=0.5, rely=.1, anchor=CENTER)
        
        sliderCol = customtkinter.CTkSlider(self.buildingFrame, from_=5, to=25, variable=self.columnSize, command=slidingCol)
        sliderCol.place(relx=0.5, rely=.2, anchor=CENTER)
        sliderCol.set(5)

        labelColumn = customtkinter.CTkLabel(self.buildingFrame, text= sliderCol.get())
        labelColumn.place(relx=0.5, rely=.3, anchor=CENTER)

        # Row Selector and labels
        label1 = customtkinter.CTkLabel(self.buildingFrame, text="Select row size")
        label1.place(relx=0.5, rely=.4, anchor=CENTER)
        
        sliderRow = customtkinter.CTkSlider(self.buildingFrame, from_=5, to=25, variable=self.rowSize, command=slidingRow)
        sliderRow.place(relx=0.5, rely=.5, anchor=CENTER)
        sliderRow.set(5)

        labelRow = customtkinter.CTkLabel(self.buildingFrame, text= sliderRow.get())
        labelRow.place(relx=0.5, rely=.6, anchor=CENTER)
        
        # Game creation
        startButton = customtkinter.CTkButton(self.buildingFrame, text="Start game", command=lambda: [self.startGame()])
        startButton.place(relx=0.5, rely=.7, anchor=CENTER)

        gameMode = customtkinter.CTkSwitch(self.buildingFrame, text="Light or Dark", command=changeMode)
        gameMode.place(relx=.03, rely=.93)

        self.root.mainloop()

        
    #Removes main frame and queues the main game
    def startGame(self):
        self.buildingFrame.pack_forget()
        self.createGame(math.floor(self.columnSize.get()),math.floor(self.rowSize.get()))

    #Creting the new geometry for the frame and GUI
    def createGame(self, col, rows):
        self.column = col
        self.row = rows

        #Setting the algorithm of the bomb placement
        self.bombNum = self.columnSize.get() + self.rowSize.get()
        self.bombOrginal = self.bombNum
        self.buttonPropabilityDefault = int((self.row + self.column)/2)
        self.buttonPropability = self.buttonPropabilityDefault


        self.HUD = customtkinter.CTkFrame(self.root, width = 120, height= 40) #bg_color="green"
        self.HUD.grid(row=0, column=0, padx=20, pady=20)
        self.game = customtkinter.CTkFrame(self.root, width = (self.row *40), height= (self.column*70)) #bg_color="green"
        self.game.grid(row=1, column=0, padx=20, pady=20)
        self.bottomHUD = customtkinter.CTkFrame(self.root, width = 120, height= 40) #bg_color="green"
        self.bottomHUD.grid(row=2, column=0, padx=20, pady=20)

        geo = "%dx%d" % (self.column *70 , self.row*100)
        self.root.geometry(geo)

        #Top HUD
        self.bombLabel = customtkinter.CTkLabel(self.HUD, text="Bombs remaining: " + str(int(self.bombOrginal - len(self.bombMarked))))
        self.bombLabel.grid(row=0, column=0, padx=20, pady=20)

        fullScreenButton = customtkinter.CTkButton(self.bottomHUD, text="Full Screen", command=lambda: [self.fullScreenCommand()])
        fullScreenButton.grid(row=0, column=0, padx=20, pady=20)
        restartButton = customtkinter.CTkButton(self.bottomHUD, text="Restart", command=lambda: [self.restartCommand(self.root)])
        restartButton.grid(row=0, column=1, padx=20, pady=20)
        

        #Placing the buttons in a grid and creating a board
        for i in range(self.row):
            for j in range(self.column):
                temp = Btn("    ", i, j, 'white', self, self.game)
                self.btnList[i].append(temp)
            self.btnList.append([])

        
        #Bottom HUD
        hintLabel = customtkinter.CTkButton(self.HUD, text="Hint", command=lambda: [self.startGame()])
        hintLabel.grid(row=0, column=1, padx=20, pady=20)

    def createPostGame(self):
        #Creates the After Game Page
        self.afterGame = customtkinter.CTk()
        self.afterGame.geometry("500x500")
        self.afterGame.title("MineSweeper")
        

    def gameLost(self):
        self.root.destroy()
        self.createPostGame()
        self.afterGame.title("Game Lost")

        self.bombImage = customtkinter.CTkImage( Image.open("Images/bomb.png"), size=(90, 100))
        self.explosionImage = customtkinter.CTkImage( Image.open("Images/explosion.png"), size=(1, 1))

        self.afterGameLabel = lbl(self.afterGame, 110, 120, "Game Ended", None, self)
        self.afterGameLabel.place(.5,.5)
        self.afterGameLabel.lab.configure(fg_color="red")

        self.bombLabelLeft = lbl(self.afterGame, 90, 100, "", self.bombImage, self)
        self.bombLabelLeft.place(.2,.5)
        self.bombLabelRight = lbl(self.afterGame, 90, 100,"" , self.bombImage, self)
        self.bombLabelRight.place(.8, .5)
        self.explosionLabelLeft = lbl(self.afterGame, 90, 100, "", self.explosionImage, self)
        self.explosionLabelLeft.place(.2, .5)
        self.explosionLabelRight = lbl(self.afterGame, 90, 100, "", self.explosionImage, self)
        self.explosionLabelRight.place(.8, .5)

        self.replayButton = customtkinter.CTkButton(self.afterGame, text="Play Again", command=lambda: [self.restartCommand(self.afterGame)])
        self.replayButton.place(relx=.3, rely=.7)

        self.showBoardButton = customtkinter.CTkButton(self.afterGame, text="See Board", command=lambda: [self.showBoard()])
        self.showBoardButton.place(relx=.7, rely=.7)




        self.lostAnimation()
        self.afterGame.mainloop()

    def lostAnimation(self):
        self.afterGameLabel.lab.configure(height = self.growEffect(self.afterGameLabel.lab.winfo_height(), 150, 50, 1, self.afterGameLabel, False))
        self.afterGameLabel.lab.configure(width = self.growEffect(self.afterGameLabel.lab.winfo_width(), 150, 50, 1, self.afterGameLabel, False))
        
        tempH, tempW = self.explosionImage._size
        self.explosionImage.configure(size=(self.growEffect(tempH, 150, 1, 4, self.explosionLabelLeft, True), self.growEffect(tempW, 150, 1, 4, self.explosionLabelLeft, True)))
        self.explosionLabelLeft.lab.configure(height=tempH) 
        self.explosionLabelLeft.lab.configure(width=tempW) 
        self.explosionLabelRight.lab.configure(height=tempH) 
        self.explosionLabelRight.lab.configure(width=tempW) 
        self.afterGame.after(1000, self.lostAnimation)
    
    def growEffect(self, objVal,  max, min, acceleration, obj, startOne):
        print(obj.growing)
        if obj.growing:
            if objVal >= max:
                if startOne:
                    objVal = 1
                else:
                    obj.growing = False
            else:
                objVal += acceleration
        else:
            if objVal <= min:
                obj.growing = True
            else:
                objVal -= acceleration
        
        return objVal
        

    def gameWon(self):
        self.createPostGame()
        self.afterGame.title("Game Won")
        self.afterGameLabel.place(relx=.5,rely=.5, relheight=self.afterGameLabelHeight, relwidth=self.afterGameLabelWidth)
        self.afterGame.mainloop()
        print("You won!")


    #Checks to see is the squares surrounding the buttons are in range and if they are bombs
    def checkAround(self, btn):
        bombsAround = 0
        for i in range(-1,2):
            for j in range(-1,2):
                if (btn.column - j >= 0 and btn.column - j < self.column) and (btn.row - i >= 0 and btn.row - i < self.row):
                    temp = self.btnList[btn.row - i][btn.column - j]
                    if self.bombChecker(temp.column, temp.row):
                        bombsAround = bombsAround + 1
        
        #Recursive function that presses tiles with 0 bombs around them to make the game less tedious
        if bombsAround == 0:
            for i in range(-1,2):
                for j in range(-1,2):
                    if (btn.column - j >= 0 and btn.column - j < self.column) and (btn.row - i >= 0 and btn.row - i < self.row):
                        if self.btnList[btn.row - i][btn.column - j] not in self.visitedTile:
                            self.btnList[btn.row - i][btn.column - j].tileClick(self)

        return bombsAround
    
    #Checks if the tile has a bomb on it
    def bombChecker(self, col, rows):
        return self.btnList[rows][col].isBomb
    
    #Places the bombs after first click
    def placeBombs(self, btn):
        self.placeSafeSpace(btn)
        for i in range(len(self.btnList) - 1):
            for j in range(len(self.btnList[i])):
                if self.bombNum > 0:
                    if not self.btnList[i][j].safeSpace:
                        if btn.coinFlip(self):
                            self.btnList[i][j].isBomb = bool(True)
                            temp = self.btnList[i][j]
                            temp.btn.configure(fg_color = 'red')
                            self.bombNum = self.bombNum - 1
                else:
                    return False
                
        #Makes sure that all the bombs are placed 
        while self.bombNum > 0:
            temp = self.btnList[random.randint(0,self.row - 1)][random.randint(0,self.column - 1)]
            if not temp.isBomb and not temp.safeSpace:
                temp.isBomb = True
                self.bombNum = self.bombNum -1
                temp.btn.configure(fg_color = 'red')
    
    #creates a safe space around the first click
    def placeSafeSpace(self, btn):
        for i in range(-1,2):
            for j in range(-1,2):
                if (btn.column - j >= 0 and btn.column - j < self.column) and (btn.row - i >= 0 and btn.row - i < self.row):
                    temp = self.btnList[btn.row - i][btn.column - j]
                    temp.safeSpace = True

    #Prints text in the output to paint the board in text (x=bomb, o=not bomb)
    def printTextBoard(self):
        temp = ""
        for i in range(len(self.btnList) - 1):
            for j in range(self.column):
                if (self.btnList[i][j].isBomb):
                    temp = temp + "x"
                elif not self.btnList[i][j].isBomb:
                    temp = temp+ "o"
            print(temp)
            temp = ""

    def restartCommand(self, frame):
        frame.destroy()
        self.__init__()

    def fullScreenCommand(self):
        if self.root.attributes('-fullscreen') ==  False:
            self.root.attributes('-fullscreen',True)
        else:
            self.root.attributes('-fullscreen',False)

    def showBoard(self):
        None
        self.revealedBoard =  customtkinter.CTk()
        self.afterGame.geometry("500x500")
        self.afterGame.title("Revealed Board")

        for i in range(self.row):
            for j in range(self.column):
                self.btnList[i][j].btn.configure(master=self.revealedBoard)





        self.revealedBoard.mainloop()

    

#Customized button class to hold important variables about each button    
class Btn():
    def __init__(self,  text, r, col, color=None, board = None, master=None):
        self.text = text
        self.row = r
        self.column = col
        self.board = board
        self.color = color
        self.isBomb = False

        self.safeSpace = False

        self.btn = customtkinter.CTkButton(self.board.game, text="   ", command=lambda: self.tileClick(board), width=30)
        self.btn.grid(row=self.row, column=self.column, padx=2, pady=2)

        super().__init__()
        if self.isBomb:
            self.btn.configure(fg_color = 'red')
        else:
            self.btn.configure(fg_color = 'white')
        self.btn['text'] = self.text
        # self.btn['command'] = lambda: self.tileClick(board)
        self.btn.bind("<Button-3>", self.rightClick)

    def coinFlip(self, board):
        if random.randint(0,board.buttonPropability) == board.buttonPropability:
            board.buttonPropability = board.buttonPropabilityDefault
            return True
        else:
            board.buttonPropability = board.buttonPropability - 1
        return False
        
    def tileClick(self, board):
        # if self.btn['bg'] == 'white':
        if True:
            if not board.bombsPlaced:
                board.bombsPlaced = True
                board.placeBombs(self)
            if self.isBomb:
                self.board.gameLost()
            else:
                board.visitedTile.append(self)
                self.btn.configure(text=board.checkAround(self))
                self.colorChange()
                if len(self.board.visitedTile) == self.board.column * self.board.row -self.board.bombOrginal:
                    self.board.gameWon()
            self.btn.configure(state = "disabled")
    
    def colorChange(self):
        if self.btn.cget("text") == 0:
            self.btn.configure(fg_color = 'lightgray')
        if self.btn.cget("text") == 1:
            self.btn.configure(fg_color = 'lightblue')
        if self.btn.cget("text") == 2:
            self.btn.configure(fg_color = 'lightgreen')
        if self.btn.cget("text") == 3:
            self.btn.configure(fg_color = 'pink')
        if self.btn.cget("text") == 4:
            self.btn.configure(fg_color = 'yellow')
        if self.btn.cget("text") == 5:
            self.btn.configure(fg_color = 'red')
        if self.btn.cget("text") == 6:
            self.btn.configure(fg_color = 'purple')
        else:
            return
    
    def rightClick(self, e):
        if self.btn.cget("fg_color") == 'white':
            self.btn.configure(fg_color = 'red')
            self.board.bombMarked.append(self)
        elif self.btn.cget("fg_color") == 'red':
            self.btn.configure(fg_color = 'white')
            self.board.bombMarked.remove(self)
        self.board.bombLabel.configure(text="Bombs remaining: " + str(int(self.board.bombOrginal) - len(self.board.bombMarked)))

class lbl():
    def __init__(self, r, h, w, t, i, board):
        self.root = r
        self.height =h
        self.width = w
        self.text = t
        self.image = i
        self.frame = board
        self.lab = customtkinter.CTkLabel(self.root, text=self.text, height = self.height, width= self.width, image=self.image)
        self.growing = True
    
    def place(self, x, y):
        self.lab.place(relx=x, rely=y, anchor="center")

    

    

MainGUI()