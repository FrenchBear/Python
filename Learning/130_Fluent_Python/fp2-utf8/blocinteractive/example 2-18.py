# Example 2-18. Bytecode for the expression s[a] += b

>>> dis.dis('s[a] += b')
  1           0 LOAD_NAME                0 (s)
              3 LOAD_NAME                1 (a)
              6 DUP_TOP_TWO
              7 BINARY_SUBSCR
              8 LOAD_NAME                2 (b)
             11 INPLACE_ADD
             12 ROT_THREE
             13 STORE_SUBSCR
             14 LOAD_CONST               0 (None)
             17 RETURN_VALUE
