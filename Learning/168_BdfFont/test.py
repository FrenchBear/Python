# pat = [ 0x70, 0x88, 0x08, 0x10, 0x20, 0x00, 0x20, ]

# for p in pat:
#     s = f"{p:08b}".replace('0', '.').replace('1', '#')
#     print(s)

i=32
while i<128:
    s=''
    for j in range(8):
        c = i+j
        if c==ord("'") or c==ord("\\"):
            s+='\\'
        s+=chr(c)
    
    print(f'<local:Segment14Screen8 Value="{s}" Width="400" />')
    i+=8
