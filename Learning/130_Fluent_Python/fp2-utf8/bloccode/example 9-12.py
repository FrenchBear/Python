# Example 9-12. A broken higher-order function to calculate a running average without keeping all history

def make_averager():
    count = 0
    total = 0

    def averager(new_value):
        count += 1
        total += new_value
        return total / count

    return averager
