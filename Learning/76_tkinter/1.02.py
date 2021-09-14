import tkinter as tk
root = tk.Tk()
label = tk.Label(root)
button = tk.Button(root)
label.config(text="I am a label widget")
button.config(text="I am a button")
label.pack()
button.pack()
root.mainloop()
