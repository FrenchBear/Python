# Learning Pandas
# 2021-03-01    PV
# https://www.learndatasci.com/tutorials/python-pandas-tutorial-complete-introduction-for-beginners/

import pandas as pd

data = {
    'apples': [3, 2, 0, 1, 4, 3], 
    'oranges': [0, 3, 7, 2, 5, 0]
}

# Create from scratch
# Each (key, value) item in data corresponds to a column in the resulting DataFrame.
# By default, the Index of this DataFrame was given to us on creation as the numbers 0-3
purchases = pd.DataFrame(data)
print(purchases)

pp = purchases[purchases.oranges>0]
print(pp)