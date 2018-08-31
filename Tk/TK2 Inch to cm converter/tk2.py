# tk2.py
# Conversion in->cm in tk
#
# 2018-08-31    PV

from tkinter import Frame, Label, Entry, StringVar, Button, messagebox, Menu
import re

NUMBER_RE = re.compile(r"(\+|-)?((\d+)|(\d+\.\d*)|(\d*\.\d+))")


# Extends the Frame class.
class MyQuitter(Frame):
    def __init__ (self, master = None):
        Frame.__init__(self, master)
        #self.pack()
        Button(self, text = "Quit",  command = self.myquit).grid()
        #b.pack(side = LEFT, expand = YES, fill = BOTH)

    def myquit(self):
        if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
            Frame.quit(self)


class MyApp(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        self.master.minsize(300, 200)
        self.master.title("Convert in -> cm")


        # Create a menu instance,
        self.mbar = Menu(self)
        # Attach to the root window.
        self.master.config(menu = self.mbar)
        # Create a new menu instance...
        self.filemenu = Menu(self.mbar, tearoff = 0)
        # ...and stick into the menu bar.
        self.mbar.add_cascade(label = "File", menu = self.filemenu)
        # Add entries to file menu.
        self.filemenu.add_command(label = "Clear", command = self.clear)
        self.filemenu.add_command(label = "Quit", command = self.main_quit)


        # Default action on Enter key
        self.master.bind("<Return>", self.key_return_event)


        Label(self, text="Length in inches:").grid(padx=6, pady=6)

        self.txt = StringVar()

        self.ent = Entry(self, textvariable=self.txt, bg="Cyan", width=7)
        self.ent.grid(row=0, column=1, padx=6, pady=6)
        self.ent.focus()

        Button(self, text="Convert", command=self.btnCalc_click).grid(row=0, column=2, padx=6, pady=6)

        self.lblRes = Label(self, text='No value', fg="Blue")
        self.lblRes.grid(columnspan=3, padx=6, pady=6)

        self.btnQuit = MyQuitter(self)
        self.btnQuit.grid(row=0, column=3, padx=6, pady=6)

        # Intercept window direct closing
        self.master.protocol("WM_DELETE_WINDOW", self.btnQuit.myquit)
    

    def main_quit(self):
        self.btnQuit.myquit()

    
    def clear(self):
        self.txt.set("")
        self.btnCalc_click()


    def btnCalc_click(self):
        v = self.txt.get()
        if v == "":
            out = 'No value'
        elif NUMBER_RE.fullmatch(v):
            cm = 2.54*float(v)
            out = f"{cm} cm"
        else:
            out = "*** Err not numeric"
            messagebox.showerror("in->cm", "Error: input is not numeric")            

        print(out)
        self.lblRes.configure(text=out)


    def key_return_event(self, event):
        self.btnCalc_click()

if __name__ == "__main__":
    MyApp().mainloop()
