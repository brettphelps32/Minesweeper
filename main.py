import tkinter as tk
from tkinter import *

class MainGUI:
    def __init__(self):

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
        self.createGame(self.columnSize.get(),self.rowSize.get())
        # GameGUI(self.columnSize.get, self.rowSize.get())


    def createGame(self, col, row):
        self.game = Tk()
        geo = "%dx%d" % (col *40 , row*40)
        self.game.geometry(geo)
        self.btnList = [[]]

        self.game.title("MineSweeper")
        mineGrid = tk.Frame(self.game)
        for i in range(col):
            for j in range(row):
                mineGrid.columnconfigure(i, weight=1)
                self.btnList[i].append(tk.Button(mineGrid, text="    ", command=lambda: [self.tileClick(i,j)]))
                self.btnList[i][j].grid(row=j, column=i)
            self.btnList.append([])
        mineGrid.pack()

    def tileClick(self, col, row):
        print("clicked")
        self.btnList[col][row].configure(bg="blue")
        

    

MainGUI()