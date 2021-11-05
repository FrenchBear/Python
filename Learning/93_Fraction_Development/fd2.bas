$ScreenHide
$Console
_Dest _Console

5 ' FracPer.bas - Print fraction period in VB without using arrays (but O(d^2) time)
6 ' 2021-11-03 PV
10 n = 100: d = 23: GoSub 30 ' 4.[3478260869565217391304]
20 n = 1: d = 9801: GoSub 30 ' 0.[000102030405060708091011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556575859606162636465666768697071727374757677787980818283848586878889909192939495969799]
21 n = 679: d = 550: GoSub 30
22 n = 1: d = 3: GoSub 30
23 n = 8: d = 4: GoSub 30
25 n = 0: d = 4: GoSub 30
26 n = 4: d = 0: GoSub 30
27 n = 0: d = 0: GoSub 30
28 End

30 Print: Print n; "/"; d; "= ";
32 If d = 0 And n = 0 Then Print "0/0 Undefined": Return
34 If d = 0 Then Print "/0 Error": Return
35 n0 = n
40 n = n Mod d
50 l = 0
60 k = 0
70 For i = 0 To d - 1
    90 'Print "i="; i; " "; n
    110 If n = 0 Then k = 1: GoTo 200
    120 m = n0 Mod d
    130 For j = 0 To i - 1
        '135 Print "  j="; j; " "; m
        140 l = l + 1
        150 If n = m Then k = 2: GoTo 200
        160 m = (m * 10) Mod d
    170 Next
    180 n = (n * 10) Mod d
190 Next
200 n = n0
210 Print Mid$(Str$(n \ d), 2);
215 n = n Mod d
217 If n = 0 Then 300
218 Print ".";
220 For i = 0 To d - 1
    230 If k = 2 And i = j Then Print "[";
    240 n = n * 10
    250 dec = n \ d
    260 n = n Mod d
    270 Print Mid$(Str$(dec), 2);
    280 If n = m And i >= j Then Print "]";: GoTo 300
    290 If n = 0 Then 300
295 Next
300 Print
310 Print l; "iterations"
320 Return