# else.py
# Play with else statement

# for
# The else block will run only if and when the for loop runs to completion (i.e., not if the for is aborted with a break).

for i in range(1, 6):
    print(i, i * i)
else:
    print("Done")
print()

for i in range(1, 6):
    print(i, i * i)
    if i == 2:
        break
else:
    print("Done")
print()

for item in ['apple', 'orange', 'cherry']:
    if item == 'banana':
        break
else:
    #raise ValueError('No banana flavor found!')
    print('ValueError: No banana flavor found!')
print()

# while
# The else block will run only if and when the while loop exits because the condition became falsy (i.e., not if the while is aborted with a break).
i = 1
while i <= 5:
    print(i, i * i)
    i += 1
else:
    print("Done")
print()

i = 1
while i <= 5:
    print(i, i * i)
    i += 1
    if i == 3:
        break
else:
    print("Done")
print()

# try
# The else block will run only if no exception is raised in the try block. The official docs also state: “Exceptions in the else clause are not handled by the preceding except clauses”.
try:
    print("try block 1")
except Exception as ex:
    print("except block", ex)
else:
    print("else block")
finally:
    print("finally block")
print()

try:
    print("try block 2")
    d = 1/0
except Exception as ex:
    print("except block 2", ex)
else:
    print("else block 2")
finally:
    print("finally block 2")
print()
