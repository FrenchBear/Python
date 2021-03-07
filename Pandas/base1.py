# Learning Pandas
# 2021-02-27    PV
# https://www.learndatasci.com/tutorials/python-pandas-tutorial-complete-introduction-for-beginners/

import pandas as pd

data = {
    'apples': [3, 2, 0, 1], 
    'oranges': [0, 3, 7, 2]
}

# Create from scratch
# Each (key, value) item in data corresponds to a column in the resulting DataFrame.
# By default, the Index of this DataFrame was given to us on creation as the numbers 0-3
purchases = pd.DataFrame(data)
print(purchases)

# We can specify the index
purchases = pd.DataFrame(data, index=['June', 'Robert', 'Lily', 'David'])
print(purchases)

# Locate order using customer name:
print(purchases.loc['Robert'])

print(purchases.loc['Robert'].apples)
