# txtfont.py
# Convert a .txt font file to compact C# representation.
#
# 2025-12-06    PV      First version

source = r'C:\Development\GitHub\CPP\810_psf_fonts\nafe\BuildNafe\Std_5x7.txt'

with open(source, encoding='437') as f:
    lines = f.readlines()

li = iter(lines)
while True:
    try:
        line = next(li).strip()
    except StopIteration:
        break
    if not line.startswith('++---'):
        continue

    asc = int(line[5:8])
    if asc<32 or asc>126:
        continue

    s = ''
    for i in range(7):
        line = next(li)
        byte = 0
        for j in range(5):
            if line[j] == 'X':
                byte |= (1 << (7 - j))
        s += f'0x{byte:02X}, '
    
    print(f"{{'{chr(asc)}', new byte[] {{ {s}}} }},")
