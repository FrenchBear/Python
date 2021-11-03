# Fraction Development 1
# 2021-10-23    PV      First version with dictionary and string, O(d) memory and O(d) time

# ToDo: sign, /0
def develop(n: int, d:int) -> str:
    dic: dict[int, int] = {}
    sint = str(n//d) + '.'
    n %= d
    sfrac = ''
    for i in range(d):
        n *= 10
        dec = n//d
        n %= d

        if n==0:    # division ends
            return sint+sfrac

        if n in dic:    # found period
            return sint+sfrac[:dic[n]]+'['+sfrac[dic[n]:]+']'
        
        # record position for reminder and decimal, and continue to next decimal
        dic[n] = i
        sfrac += str(dec)

    return ''

#print(develop(1,9801))
# Decimals .[00 01 02 03 ... 96 97 99]
# 0.[000102030405060708091011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556575859606162636465666768697071727374757677787980818283848586878889909192939495969799]

print(develop(100,23))
