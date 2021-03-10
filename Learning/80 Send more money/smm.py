# send+more=money puzzle
# 2021-03-10    PV

for s in range(1,10):
    for e in range(1,10):
        if e!=s:
            for n in range(1,10):
                if n not in (s,e):
                    for d in range(1,10):
                        if d not in (s,e,n):
                            for m in range(1,10):
                                if m not in (s,e,n,d):
                                    for o in range(1,10):
                                        if o not in (s,e,n,d,m):
                                            for r in range(1,10):
                                                if r not in (s,e,n,d,m,o):
                                                    for y in range(1,10):
                                                        if y not in (s,e,n,d,m,o,r):
                                                            if s*1000+e*100+n*10+d+m*1000+o*100+r*10+e==m*10000+o*1000+n*100+e*10+y:
                                                                print(s,e,n,d,' + ',m,o,r,e,' = ',m,o,n,e,y)

