import Tkinter as tk
import tkMessageBox
import sys
import os

class App(tk.Tk):
    b1 = "up"
    xold, yold = None, None
    color= "red"
    linesize = 2
    counter = 1 #keeps track of the current working line, is incremented as soon as line is finished
    undone = [] #keeps a list of coordinate lists on undone items

    def __init__(self):
        tk.Tk.__init__(self)
        self.drawing_area = tk.Canvas(self, width=600, height=600, background="white")
        self.drawing_area.pack()
        self.drawing_area.bind("<Motion>", self.motion)
        self.drawing_area.bind("<ButtonPress-1>", self.b1down)
        self.drawing_area.bind("<ButtonRelease-1>", self.b1up)

        self.button1 = tk.Button(self, text = "Reset", command = self.blank_canvas, anchor = tk.N)
        self.button1.configure(width = 3, background = "#FFFFFF", relief = tk.FLAT)
        self.button1.pack(side="left")

        self.button2 = tk.Button(self, text = "Undo", command = self.undo, anchor = tk.N)
        self.button2.configure(width = 3, background = "#FFFFFF", relief = tk.FLAT)
        self.button2.pack(side="left")

        self.button3 = tk.Button(self, text = "Redo", command = self.redo, anchor = tk.N)
        self.button3.configure(width = 3, background = "#FFFFFF", relief = tk.FLAT)
        self.button3.pack(side="left")

    def blank_canvas(self):
        self.drawing_area.delete("line")

    def undo(self):
        self.counter -= 1 #decrements the counter to look at the previous item
        currentlist = [] #creates a list to store the coordinates in
        for item in self.drawing_area.find_withtag("line"+str(self.counter)): #find all sub lines from the previous line
            currentlist.append(self.drawing_area.coords(item)) #get and add the coordinates to the working list
        self.drawing_area.delete("line"+str(self.counter)) #delete all items of the current line
        self.undone.append(currentlist) #add the working list to the stored list

    def redo(self):
        try:
            currentlist = self.undone.pop() #fetch and remove last set of coordinates
            for coords in currentlist: #for set of coordinates redraw subline
                self.drawing_area.create_line(coords,smooth=tk.TRUE,fill = self.color, width=self.linesize, tags=["line", "line"+str(self.counter)])
            self.counter += 1 #re increment counter
        except IndexError:
            pass #occurs if list is empty

    def b1down(self, event):
        self.b1 = "down"

    def b1up(self, event):
        self.b1 = "up"
        self.xold = None
        self.yold = None
        self.counter += 1

    def motion(self, event):
        if self.b1 == "down":
            if self.xold is not None and self.yold is not None:
                event.widget.create_line(self.xold,self.yold,event.x,event.y,smooth=tk.TRUE,fill = self.color, width=self.linesize, tags=["line", "line"+str(self.counter)])
            self.xold = event.x
            self.yold = event.y

if __name__ == "__main__":
    app = App()
    app.mainloop()