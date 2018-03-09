
import os
from shutil import copyfile

path = r'C:\Temp\BTB'
files = os.scandir(path)
n=24
f=0
for entry in files:
    n += 1
    if n>24:
        n = 1
        f += 1
        fo = path + '\\' + ('%02d'%f)
        print(fo)
        os.mkdir(fo, 0o777)
    copyfile(path+'\\'+entry.name, fo+'\\'+entry.name)
             
