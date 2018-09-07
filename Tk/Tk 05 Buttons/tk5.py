# tk5 - Learning Tk #5
# Buttons show case
# From http://www.java2s.com/Code/Python/GUI-Tk/ButtonBorderstyles.htm
#
# 2018-09-01    PV

import tkinter as tk


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Button Styles')
        for bdw in range(5):
            setattr(self, 'of%d' % bdw, tk.Frame(self.root, borderwidth=0))
            tk.Label(getattr(self, 'of%d' % bdw),
                    text='border width = %d  ' % bdw).pack(side=tk.LEFT)
            for relief in [tk.RAISED, tk.SUNKEN, tk.FLAT, tk.RIDGE, tk.GROOVE, tk.SOLID]:
                tk.Button(getattr(self, 'of%d' % bdw), text=relief, borderwidth=bdw,
                        relief=relief, width=10,
                        command=lambda s=self, r=relief, b=bdw: s.prt(r,b))\
                            .pack(side=tk.LEFT, padx=7-bdw, pady=7-bdw)
            getattr(self, 'of%d' % bdw).pack()

    def prt(self, relief, border):
        print('%s:%d' % (relief, border))

myGUI = GUI()
myGUI.root.mainloop()
