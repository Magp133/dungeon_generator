"""
File used to test and check the functionality of the code.
"""

import pandas as pd

# import the items database
items = pd.read_csv('data/Items_magic.csv')

# remove items that have a rarity of none.
# creating the magical items database
items = items[items['Rarity'] != 'none']

# remove the value column
items = items.drop(columns=['Value'])

# save the file
items.to_csv('data/Items_magic.csv', index=False)

print(items.head())