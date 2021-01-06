import tkinter as tk
import tkinter.font as tkFont


from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
FR_PRIVATE  = 0x10
FR_NOT_ENUM = 0x20

# https://stackoverflow.com/questions/11993290/truly-custom-font-in-tkinter
def loadfont(fontpath, private=True, enumerable=False):
    '''
    Makes fonts located in file `fontpath` available to the font system.
    `private`     if True, other processes cannot see this font, and this font will be unloaded when the process dies
    `enumerable`  if True, this font will appear when enumerating fonts

    See https://msdn.microsoft.com/en-us/library/dd183327(VS.85).aspx
    '''
    if isinstance(fontpath, str):
        pathbuf = create_unicode_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExW
    else:
        raise TypeError('fontpath must be of type str')

    flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
    numFontsAdded = AddFontResourceEx(byref(pathbuf), flags, 0)
    return bool(numFontsAdded)


# Main form
root = tk.Tk()
root.title('Python Tk Custom Font')

# Load extra fonts
loadfont(r'X:\Fonts\Individual Fonts\Flexo\Flexo-Regular.otf')

# Fonts used
lf = ('Segoe UI Semibold', 12)  # Label Font
tf = ('Segoe UI', 11)           # Text Font
ff = ('Iosevka', 10)            # Fixed font
fl = ('Flexo', 12)              # Flexo-Regular.ttf

tk.Label(root, text='Label 1 Segoe UI Semibold 12', font=lf).pack()
tk.Label(root, text='Label 2 Segoe UI 11', font=tf).pack()
tk.Label(root, text='Label 3 Iosevka 10', font=ff).pack()
tk.Label(root, text='Label 4 Flexo 12', font=fl).pack()

root.mainloop()
