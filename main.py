import tkinter as tk
from tkinter import *





class GameGUI:
    def __init__(self):
        self.root = Tk()    

        self.root.geometry("500x500")
        self.root.title("MineSweeper")

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

        startButton = tk.Button(self.root, text="Start game", command=lambda: [self.startGame(), self.root.destroy])
        startButton.pack(pady=50)



        self.root.mainloop()

    def startGame(self):
        print(str(self.columnSize.get()) + "," + str(self.rowSize.get()))
        self.createGame(self.columnSize.get(),self.rowSize.get())

    def createGame(self, col, row):
        print("Starting Game")

    

MainGUI()