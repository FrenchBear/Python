Option Explicit
'Option Compare Text

' Fraction Development 2
' For each new decimal found, restart division from the beginning to see if that decimal has already been found
' Bad algorithm in O(n²) where n is period length, but on simple programmable calculators, we have no choice
' if we want to allow large denominators such as 9801 in the test since we potentially need an array of 9801 integers
'
' 2021-11-03    PV      Second version using O(1) memory (sint does not really count) but O(d²) time
' 2021-11-05    PV      Sign; /0; tests
' 2022-06-26    PV      VB6/VBScript version

Function Develop(n, d)
    If d = 0 Then
        If n <> 0 Then
            Develop = "/0 error"
        Else
            Develop = "0/0 undefined"
        End If
        Exit Function
    End If

    Dim sint
    sint = ""
    If n < 0 Or d < 0 Then
        If n * d < 0 Then
            sint = "-"
        End If
        n = Abs(n)
        d = Abs(d)
    End If
    sint = sint & CStr(n \ d)
    n = n Mod d
    If n = 0 Then
        Develop = sint
        Exit Function
    End If
    sint = sint & "."

    Dim n0, k, i, j, m, dec
    n0 = n
    k = 0
    For i = 0 To d - 1
        If n = 0 Then    ' division ends
            k = 1
            Exit For
        End If

        m = n0 Mod d
        For j = 0 To i - 1
            If n = m Then
                ' Found a repeating remainder, it's periodic
                k = 2
                Exit For
            End If
            m = m * 10
            ' no need to compute decimal
            ' decl = m//d
            m = m Mod d
        Next

        If k > 0 Then Exit For

        n = n * 10
        dec = n \ d
        n = n Mod d
    Next

    n = n0 Mod d
    For i = 0 To d - 1
        If k = 2 And i = j Then
            sint = sint & "["
        End If
        n = n * 10
        dec = n \ d
        n = n Mod d
        sint = sint & CStr(dec)
        If n = m And i >= j Then
            Develop = sint + "]"
            Exit Function
        End If
        If n = 0 Then
            Develop = sint
            Exit Function
        End If
    Next

End Function


' print(develop(1,9801))
' Decimals .[00 01 02 03 ... 96 97 99]
' 0.[000102030405060708091011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556575859606162636465666768697071727374757677787980818283848586878889909192939495969799]

Sub test(n, d, r)
    Dim x
    x = Develop(n, d)
    If x = r Then
        Wscript.Echo "Ok: " & n & "/" & d & " = " & r
    Else
        Wscript.Echo "KO: " & n & "/" & d & " found " & x & " expected " & r
    End If
End Sub


Sub Main()
    Wscript.Echo Develop(1, 3)
    
    test 100, 250, "0.4"
    test 100, 4, "25"
    test 8, 2, "4"
    test 1, 3, "0.[3]"
    test -1, 3, "-0.[3]"
    test 1, -3, "-0.[3]"
    test -1, -3, "0.[3]"
    test 1, 5, "0.2"
    test 1, 7, "0.[142857]"
    test 100, 23, "4.[3478260869565217391304]"
    test 679, 550, "1.23[45]"
    test 0, 5, "0"
    test 5, 0, "/0 error"
    test 0, 0, "0/0 undefined"

    Dim t, i
    t = Timer
    For i = 1 To 100000
        Develop 100, 23
    Next
    t = Timer - t
    Wscript.Echo "Elapsed #2: " & t & " s"
End Sub

Main()
