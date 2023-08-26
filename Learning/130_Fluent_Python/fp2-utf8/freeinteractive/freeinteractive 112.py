>>> brl = 1 / 4.82  # BRL to USD currency conversion rate
>>> brl
0.20746887966804978
>>> format(brl, '0.4f')
'0.2075'
>>> '1 BRL = {rate:0.2f} USD'.format(rate=brl)
'1 BRL = 0.21 USD'
>>> f'1 USD = {1 / brl:0.2f} BRL'
'1 USD = 4.82 BRL'
