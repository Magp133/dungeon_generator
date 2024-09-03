"""
File used to test and check the functionality of the code.
"""

import pandas as pd

# import the items database
items = pd.read_csv('data/Items_magic.csv')

# remove the items with no Value which is NA
#extract the mundance items which do not have a rarity.
# their rarity is 
mundane_items = items[items['Rarity'] == 'none']

#drop the rarity column
mundane_items = mundane_items.drop(columns=['Rarity'])
# drop the attunement table
mundane_items = mundane_items.drop(columns=['Attunement'])

# save the items.csv file
mundane_items.to_csv('data/Items.csv', index=False)

print(mundane_items.head())