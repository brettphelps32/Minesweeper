import tkinter as tk
from tkinter import *
import random

class MainGUI:
    def __init__(self):
        self.btnList = [[]]
        self.root = Tk()    

        self.root.geometry("500x500")
        self.root.title("MineSweeper")

        label = tk.Label(self.root, text="Select column size")
        label.pack(pady = 20)

        self.columnSize = tk.IntVar()
        slider1 = Scale(self.root, from_=5, to=25, orient=HORIZONTAL, variable=self.columnSize)
        slider1.pack()

        label1 = tk.Label(self.root, text="Select row size")
        label1.pack(pady = 20)
        self.rowSize = tk.IntVar()
        slider2 = Scale(self.root, from_=5, to=25, orient=HORIZONTAL, variable=self.rowSize)
        slider2.pack()

        label2 = tk.Label(self.root, text="Number of bombs: ")
        label2.pack(pady = 40)
        
        

        startButton = tk.Button(self.root, text="Start game", command=lambda: [self.startGame()])
        startButton.pack(pady=50)

        self.root.mainloop()

    def startGame(self):
        self.root.destroy()
        self.bombNum = self.columnSize.get() + self.rowSize.get()
        self.bombOrginal = self.bombNum
        # print(self.bombNum)
        self.createGame(self.columnSize.get(),self.rowSize.get())

    def createGame(self, col, rows):
        self.game = Tk()
        self.column = col
        self.row = rows
        geo = "%dx%d" % (self.column *40 , self.row*40)
        self.game.geometry(geo)
        self.visitedTile = []

        self.buttonPropabilityDefault = int((self.row + self.column)/2)
        self.buttonPropability = self.buttonPropabilityDefault

        self.game.title("MineSweeper")
        self.mineGrid = tk.Frame(self.game)
        for i in range(self.row):
            for j in range(self.column):

                self.mineGrid.columnconfigure(i, weight=1)
                temp = Btn("    ", i, j, 'white', self)
                self.btnList[i].append(temp)
                if self.btnList[i][j].isBomb:
                    self.bombNum = self.bombNum - 1
                
            self.btnList.append([])

    def checkAround(self, btn):
        bombsAround = 0
        self.visitedTile.append(btn)
        for i in range(-1,2):
            for j in range(-1,2):
                if (btn.column - j >= 0 and btn.column - j < len(self.btnList) -1) and (btn.row - i >= 0 and btn.row - i < len(self.btnList)-1):
                    temp = self.btnList[btn.row - i][btn.column - j]
                    if self.bombChecker(temp.column, temp.row):
                        bombsAround = bombsAround + 1
        
        if bombsAround == 0:
            for i in range(-1,2):
                for j in range(-1,2):
                    if (btn.column - j >= 0 and btn.column - j < len(self.btnList) -1) and (btn.row - i >= 0 and btn.row - i < len(self.btnList)-1):
                        if self.btnList[btn.row - i][btn.column - j] not in self.visitedTile:
                            self.btnList[btn.row - i][btn.column - j].tileClick(self)
            self.clearNonTreat(btn)

        return bombsAround
    
    def bombChecker(self, col, rows):
        return self.btnList[rows][col].isBomb
    
    def clearNonTreat(self, btn):
        return

class Btn(Button):
    def __init__(self, text, r, col, color=None, board = None):
        self.text = text
        self.row = r
        self.column = col
        self.board = board
        self.color = color
        self.bombRemaining = board.bombNum
        self.isBomb = False

        

        
        
        # self.btnType(board)
        super().__init__()
        if self.isBomb:
            None
            self['bg'] = 'white'
            self['bg'] = 'red'
        else:
            self['bg'] = 'white'
        self['text'] = self.text
        self['command'] = lambda: self.tileClick(board)
        self.grid(row=self.row, column=self.column)
        self.bind("<Button-3>", self.rightClick)

    def btnType(self, board, c, r):
        tempList = board.btnList
        for i in range(len(tempList) - 1):
            for j in range(len(tempList[i])):
                if board.bombNum > 0:
                    if r+1 != i and r != i and r-1 != i:
                        print("Row "+ str(r)+ ": at " + str(i))
                        if c !=j and c-1 != j and c + 1!= j:
                            if self.coinFlip(board):
                                tempList[i][j].isBomb = bool(True)
                                temp = tempList[i][j]
                                temp['bg'] = "red"
                                board.bombNum = board.bombNum - 1
                else:
                    return False
        # while board.bombNum > 0:
        #     temp = board.btnList[random.randint(0,board.row - 1)][random.randint(0,board.column - 1)]
            
        #     if not temp.isBomb:
        #         temp.isBomb = True
        #         board.bombNum = board.bombNum -1
        #         temp['bg'] = 'red'

    def coinFlip(self, board):
        if random.randint(0,board.buttonPropability) == board.buttonPropability:
            board.buttonPropability = board.buttonPropabilityDefault
            return True
        else:
            board.buttonPropability = board.buttonPropability - 1
            return False
    

    
    def tileClick(self, board):
        if self['bg'] == 'white':
            if board.bombNum > 0:
                self.btnType(board, self.column, self.row)
            if self.isBomb:
                print('BOOM')
            else:
                self.config(text=board.checkAround(self))
                self.colorChange()
                if len(self.board.visitedTile) == self.board.column * self.board.row -self.board.bombOrginal:
                    print("Game won!")
            self.config(relief=SUNKEN)
    
    def colorChange(self):
        if self['text'] == 0:
            self['bg'] = 'lightgray'
        if self['text'] == 1:
            self['bg'] = 'lightblue'
        if self['text'] == 2:
            self['bg'] = 'lightgreen'
        if self['text'] == 3:
            self['bg'] = 'pink'
        if self['text'] == 4:
            self['bg'] = 'yellow'
        if self['text'] == 5:
            self['bg'] = 'red'
        else:
            return
    
    def rightClick(self, e):
        if self['bg'] == 'white':
            self['bg'] = 'red'
        elif self['bg'] == 'red':
            self['bg'] = 'white'
        



MainGUI()

