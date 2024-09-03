"""
File used to test and check the functionality of the code.
"""

import pandas as pd

# import the items database
items = pd.read_csv('data/Items_magic.csv')

# remove rarities that are unknown
items = items[items['Rarity'] != 'unknown']

print(items.head())

# save the items database
items.to_csv('data/Items_magic.csv', index=False)
