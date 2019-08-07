# Example of drawing

import tkinter as tk

class App:

    def __init__(self, master):
        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack()
        master.wm_title('Drawing with tk')

    def Draw(self):
        self.canvas.create_line(0, 0, 400, 200, fill='black', width=1)
        self.canvas.create_oval(50,50,150,200)

root = tk.Tk()
app = App(root)
root.wm_title('Tk example')
app.Draw()

root.mainloop()
