# Exceptions
# Learning Python
#
# 2015-05-02    PV

try:
    list = [1, 2, 3]
    x = list[3]
except IndexError:
    print('Oops!')
finally:
    print('Back to normal')

print()
try:
    n = input("Enter number:")
    print(f"{n}⁻¹ = {1/int(n)}")
except ZeroDivisionError as zd:
    print("/0:", zd)
except ValueError as ve:
    print("Value error:", ve)
else:
    print("No problem detected during calculation")
finally:
    print("Calculation is done")


print()
print('Enter words, Ctrl+C [Return] to stop')
li = []
try:
    while True:
        n = input('Enter a word: ')
        li.append(n)
except KeyboardInterrupt:
    print("Done.")

print("List:", li)
