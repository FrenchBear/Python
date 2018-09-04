# tk2 - Learning Tk #2
# Conversion in->cm in tk, my first app
# Tests various elements of Tk
#
# 2018-08-31    PV

import tkinter as tk
import tkinter.messagebox as tkmb
import re

NUMBER_RE = re.compile(r"(\+|-)?((\d+)|(\d+\.\d*)|(\d*\.\d+))")


# Extends the Frame class.
class MyQuitter(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        tk.Button(self, text="Quit",  command=self.myquit,
                  borderwidth=1, relief=tk.SOLID).grid()

    def myquit(self):
        if tkmb.askokcancel("Quit", "Do you really wish to quit?"):
            tk.Frame.quit(self)


class MyApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        self.master.minsize(300, 200)
        self.master.title("Convert in -> cm")

        # Menu
        # Create a menu instance and attach it to root window
        self.mbar = tk.Menu(self)
        self.master.config(menu=self.mbar)
        # Create a new menu instance and stick into the menu bar.
        self.filemenu = tk.Menu(self.mbar, tearoff=0)
        self.mbar.add_cascade(label="File", menu=self.filemenu)
        # Add entries to file menu.
        self.filemenu.add_command(label="Clear", command=self.clear, accelerator="Ctrl+L")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="About", command=self.about, accelerator="Ctrl+A")
        self.filemenu.add_command(label="Quit", command=self.main_quit, accelerator="Ctrl+Q")

        # Keys bindings
        self.master.bind("<Return>", self.key_return_event)         # Default action on Enter key
        self.master.bind('<Control-q>', self.main_quit_event)       # Sedicated 2-arg event function
        self.master.bind('<Control-l>', self.clear)                 # Shared event function with default value for event
        self.master.bind('<Control-a>', lambda e: self.about())     # Relay-lambda to cann single arg event function


        tk.Label(self, text="Length in inches:").grid(padx=6, pady=6)

        self.txt = tk.StringVar()

        self.ent = tk.Entry(self, textvariable=self.txt, bg="Cyan", width=7)
        self.ent.grid(row=0, column=1, padx=6, pady=6)
        self.ent.focus()

        # Convert button: Underline 1st letter and add a binding to Alt+C
        tk.Button(self, text="Convert", underline=0, command=self.btnCalc_click, borderwidth=3, relief=tk.SOLID).grid(row=0, column=2, padx=6, pady=6)
        self.master.bind('<Alt_L><c>', lambda e: self.btnCalc_click())

        self.lblRes = tk.Label(self, text='No value', fg="Blue")
        self.lblRes.grid(columnspan=3, padx=6, pady=6)

        self.btnQuit = MyQuitter(self)
        self.btnQuit.grid(row=0, column=3, padx=6, pady=6)

        # Intercept window direct closing
        self.master.protocol("WM_DELETE_WINDOW", self.btnQuit.myquit)

    def main_quit(self):
        self.btnQuit.myquit()

    # Version with event arg for shortcus binding
    def main_quit_event(self, event):
        self.main_quit()

    # dual mode version, both for direct call and as an event handler
    def clear(self, event=None):
        self.txt.set("")
        self.btnCalc_click()

    def btnCalc_click(self):
        v = self.txt.get()
        if v == "":
            out = 'No value'
        elif NUMBER_RE.fullmatch(v):
            cm = 2.54*float(v)
            out = f"{cm:.2f} cm"
        else:
            out = "*** Err not numeric"
            tkmb.showerror("in->cm", "Error: input is not numeric")

        print(out)
        self.lblRes.configure(text=out)

    def key_return_event(self, event):
        self.btnCalc_click()
    
    def about(self):
        tkmb.showinfo("in->cm", "My first tk application.\r\n© P.Violent 2018")


if __name__ == "__main__":
    MyApp().mainloop()
