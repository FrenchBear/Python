import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText  # type: ignore
from TkToolTip import TkToolTip

root = tk.Tk()

case = tk.IntVar(root, 0)
norm = tk.StringVar(root, 'None')
seq = tk.StringVar(root, 'CN')
countChars = tk.StringVar(root, "")

list_headers = ['CP', 'Name', 'Script', 'Category', 'UTF-16', 'UTF-8']

# Fonts used
lf = ('Segoe UI Semibold', 10)  # Label Font
tf = ('Segoe UI', 11)           # Text Font
ff = ('Iosevka', 10)            # Fixed font

def about_click():
    pass

def inputText_Modified(t: ScrolledText):
    pass

def Treeview_Select(evt):
    pass

tk.Label(root, text='Text', font=lf).grid(row=0, column=0, sticky='nw', padx=6, pady=6)
inputText = ScrolledText(root, height=4, width=20, wrap=tk.WORD, font=tf)
inputText.grid(row=0, column=1, sticky='we', padx=6, pady=6)
inputText.focus()
inputText.bind('<<Modified>>', lambda event: inputText_Modified(inputText))

buttonsFrame = tk.Frame(root, padx=6, pady=6)
buttonsFrame.grid(row=0, column=2, sticky='n')
aboutButton = tk.Button(buttonsFrame, text='About', command=about_click)
aboutButton.pack(fill=tk.X)
root.bind('<F1>', lambda e: about_click())
aboutButton_ttp = TkToolTip(aboutButton, '[F1] Show application information')
tk.Button(buttonsFrame, text='Close', command=lambda: tk.Frame.quit(root)).pack(fill=tk.X, pady=6)


tk.Label(root, text='Transformations', font=lf).grid(row=1, column=0, sticky='nw', padx=6, pady=6)
optionsFrame = tk.Frame(root, padx=6, pady=6)
optionsFrame.grid(row=1, column=1, sticky='nw')

buttonsFrame = tk.Frame(root, padx=6, pady=6)
buttonsFrame.grid(row=0, column=2, sticky='n')
aboutButton = tk.Button(buttonsFrame, text='About', command=about_click)
aboutButton.pack(fill=tk.X)
root.bind('<F1>', lambda e: about_click())
aboutButton_ttp = TkToolTip(aboutButton, '[F1] Show application information')

tk.Button(buttonsFrame, text='Close', command=lambda: tk.Frame.quit(root)).pack(fill=tk.X, pady=6)

caseFrame = tk.LabelFrame(optionsFrame, text='Case', font=lf)
caseFrame.pack(side=tk.LEFT, anchor='n')
tk.Radiobutton(caseFrame, text='Lowercase', variable=case, value=1).pack(anchor='w')
tk.Radiobutton(caseFrame, text='Uppercase', variable=case, value=2).pack(anchor='w')
tk.Radiobutton(caseFrame, text='None', variable=case, value=0).pack(anchor='w')

normFrame = tk.LabelFrame(optionsFrame, text='Normalization', font=lf)
normFrame.pack(side=tk.LEFT, anchor='n')
nfcOption = tk.Radiobutton(normFrame, text='NFC', variable=norm, value='NFC')
TkToolTip(nfcOption, 'NFC: Normal Form C, canonical decomposition then canonical composition')
nfcOption.pack(anchor='w')
nfdOption = tk.Radiobutton(normFrame, text='NFD', variable=norm, value='NFD')
TkToolTip(nfdOption, 'NFD: Normal Form D, canonical decomposition')
nfdOption.pack(anchor='w')
nfkcOption = tk.Radiobutton(normFrame, text='NFKC', variable=norm, value='NFKC')
TkToolTip(nfkcOption, 'NFKC: Normal Form KC, compatibility decomposition then canonical composition')
nfkcOption.pack(anchor='w')
nfkdOption = tk.Radiobutton(normFrame, text='NFKD', variable=norm, value='NFKD')
TkToolTip(nfkdOption, 'NFKD: Normal Form KD, compatibility decomposition')
nfkdOption.pack(anchor='w')
tk.Radiobutton(normFrame, text='None', variable=norm, value='None').pack(anchor='w')

seqFrame = tk.LabelFrame(optionsFrame, text='Sequence', font=lf)
seqFrame.pack(side=tk.LEFT, anchor='n')
tk.Radiobutton(seqFrame, text='Case then Normalization', variable=seq, value='CN').pack(anchor='w')
tk.Radiobutton(seqFrame, text='Normalization then Case', variable=seq, value='NC').pack(anchor='w')

tk.Label(root, text='Result', font=lf).grid(row=2, column=0, sticky='nw', padx=6, pady=6)
resultText = tk.Text(root, height=4, width=20, wrap=tk.WORD, font=tf)
resultText.grid(row=2, column=1, sticky='nsew', padx=6, pady=6)

tk.Label(root, text='Counts', font=lf).grid(row=3, column=0, sticky='nw', padx=6, pady=6)
countsFrame = tk.Frame(root, padx=6, pady=6)
countsFrame.grid(row=3, column=1, sticky='nw')
tk.Label(countsFrame, text='Chars', font=lf).pack(side=tk.LEFT, anchor='s')
tk.Label(countsFrame, textvariable=countChars, font=tf).pack(side=tk.LEFT, anchor='s')

tk.Label(root, text='Codepoints', font=lf).grid(row=4, column=0, sticky='nw', padx=6, pady=6)
listFrame = tk.Frame()
listFrame.grid(row=4, column=1, sticky='nsew', padx=6, pady=6)
cpListbox = tk.Listbox(listFrame, font=ff, width=100)
cpListbox.pack(side="left", expand=True, fill="both")
cpScroller = tk.Scrollbar(listFrame, orient="vertical")
cpScroller.pack(side="right", fill="y")
cpScroller.config(command=cpListbox.yview)
cpListbox.config(yscrollcommand=cpScroller.set)
#cpListbox.bind('<<ListboxSelect>>', cpListbox_Select)

"""
container = tk.Frame(root, padx=6, pady=6)
container.grid(row=4, column=1, sticky='nsew')
# create a Treeview with dual scrollbars
tree = ttk.Treeview(container, columns=list_headers, show="headings")
tree.pack(expand=1)
tree.bind('<<TreeviewSelect>>', Treeview_Select)
vsb = ttk.Scrollbar(orient="vertical", command=tree.yview)
hsb = ttk.Scrollbar(orient="horizontal", command=tree.xview)
tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
tree.grid(column=0, row=0, sticky='nsew', in_=container)
vsb.grid(column=1, row=0, sticky='ns', in_=container)
hsb.grid(column=0, row=1, sticky='ew', in_=container)
container.grid_columnconfigure(0, weight=1)
container.grid_rowconfigure(0, weight=1)
"""
tk.Label(root, text='Test', font=lf).grid(row=5, column=0, sticky='nw', padx=6, pady=6)
tk.Button(root, text='R5', font=tf).grid(row=5, column=1, sticky='nw', padx=6, pady=6)

countChars.set('17')

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(4, weight=1)

root.mainloop()
