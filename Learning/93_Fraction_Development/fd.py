# Fraction Development
# 2021-10-23    PV

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

print(develop(1,1089))
