# tk3 - Learning Tk #3
# Use an image in a button and update it
# Use pillow (Python Imaging Library) to show images (pip install pillow)
#
# 2018-08-31    PV


import tkinter as tk
from PIL import Image, ImageTk


class MyImage(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()

        img1 = Image.open("FrenchBear38.jpg")
        img2 = Image.open("FrenchBear38R.jpg")

        # Keep a reference!
        self.pic1 = ImageTk.PhotoImage(img1)
        self.pic2 = ImageTk.PhotoImage(img2)
        self.pic = self.pic1

        self.btn = tk.Button(self, image=self.pic, command=self.btn_click)
        self.btn.pack()

    def btn_click(self):
        if self.pic==self.pic1:
            self.pic=self.pic2
        else:
            self.pic=self.pic1

        self.btn.configure(image=self.pic)

if __name__ == "__main__":
    MyImage().mainloop()
