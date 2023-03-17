# ReformatCSInterface
#
# 2023-03-17    PV

import re

LINE = re.compile(r' +(static )?([^ ]+ )([^\.]+)\.([^\(]+\()(.*)')
#LINE = re.compile(r'\s+(static )?([^ ]+ )')

nm=0
li = ''
with open('code.cs') as source:
    while line:=source.readline():
        ma = LINE.match(line.rstrip())
        if ma:
            nm+=1
            nl = '        public '+(ma.group(1) if ma.group(1) else '')+ma.group(2)+ma.group(4)+ma.group(5)
            if ma.group(3)!=li:
                li=ma.group(3)
                print()
                print('        // '+ma.group(3))
            print(nl)
print(nm)