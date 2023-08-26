# Example 31-3. coroaverager0.py: code for a running average coroutine

def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average = total/count
