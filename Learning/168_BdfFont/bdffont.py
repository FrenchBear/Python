# bdffont.py
# Convert a .bdf font file to compact C# representation.
#
# 2025-12-06    PV      First version

source = r'C:\Development\GitHub\RPiExtra\LedMatrix\adafruit-rpi-rgb-led-matrix-master\fonts\5x7.bdf'

with open(source) as f:
    lines = f.readlines()

encoding_min = 32
encoding_max = 126

li = iter(lines)
while True:
    try:
        line = next(li).strip()
    except StopIteration:
        break

    if line.startswith('ENCODING '):
        encoding = int(line.split()[1])
        if encoding < encoding_min:
            continue
        if encoding > encoding_max:
            continue

        while True:
            line = next(li).strip()
            if line.startswith("BITMAP"):
                break
        
        s = ''
        for i in range(7):
            line = next(li).strip()
            byte = int(line, 16)
            s += f'0x{byte:02X}, '
        
        print(f"{{'{chr(encoding)}', new byte[] {{ {s}}} }},")
