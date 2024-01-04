import tkinter as tk
from tkinter import *
import random
import sys

sys.setrecursionlimit(3000)



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
        # print(self.bombNum)
        self.createGame(self.columnSize.get(),self.rowSize.get())


    def createGame(self, col, rows):
        self.game = Tk()
        self.column = col
        self.row = rows
        geo = "%dx%d" % (self.column *40 , self.row*40)
        self.game.geometry(geo)


        self.buttonPropabilityDefault = int((self.row + self.column)/2)
        self.buttonPropability = self.buttonPropabilityDefault

        self.game.title("MineSweeper")
        mineGrid = tk.Frame(self.game)
        for i in range(self.row):
            for j in range(self.column):

                mineGrid.columnconfigure(i, weight=1)
                temp = Btn("    ", i, j, 'white', self)
                self.btnList[i].append(temp)
                if self.btnList[i][j].isBomb:
                    self.bombNum = self.bombNum - 1
                
            self.btnList.append([])
        while self.bombNum > 0:
            temp = self.btnList[random.randint(0,self.row - 1)][random.randint(0,self.column - 1)]
            
            if not temp.isBomb:
                temp.isBomb = True
                self.bombNum = self.bombNum -1
                temp['bg'] = 'red'

    def checkAround(self, btn):
        bombsAround = 0
        for i in range(-1,2):
            for j in range(-1,2):
                if (btn.column - j >= 0 and btn.column - j < len(self.btnList) -1) and (btn.row - i >= 0 and btn.row - i < len(self.btnList)-1):
                    temp = self.btnList[btn.row - i][btn.column - j]
                    if self.bombChecker(temp.column, temp.row):
                        bombsAround = bombsAround + 1
        
        if bombsAround == 0:
            # for i in range(-1,2):
            #     for j in range(-1,2):
            #         if (btn.column - j >= 0 and btn.column - j < len(self.btnList) -1) and (btn.row - i >= 0 and btn.row - i < len(self.btnList)-1):
            #             self.btnList[btn.row - i][btn.column - j].tileClick(self)
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

        
        
        self.btnType(board)
        super().__init__()
        if self.isBomb:
            self['bg'] = 'red'
        else:
            self['bg'] = 'white'
        self['text'] = self.text
        self['command'] = lambda: self.tileClick(board)
        self.grid(row=self.row, column=self.column)
        

    def btnType(self, board):
        if self.bombRemaining > 0:
            if self.coinFlip(board):
                self.isBomb = bool(True)
                self.bombRemaining = self.bombRemaining - 1
        else:
            return False

    def coinFlip(self, board):
        if random.randint(0,board.buttonPropability) == board.buttonPropability:
            board.buttonPropability = board.buttonPropabilityDefault
            return True
        else:
            board.buttonPropability = board.buttonPropability - 1
            return False
    
    def tileClick(self, board):
        if self.isBomb:
            print('BOOM')
        else:
            self.config(text=board.checkAround(self))
        self.config(bg='blue')
        self.config(relief=SUNKEN)

    
        




start = MainGUI()