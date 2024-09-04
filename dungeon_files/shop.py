import pandas as pd
import random

from globals import *

class RoomShop:
    def __init__(self) -> None:
        """
        Init the shop.
        Creates a shop with items based on the difficulty of the dungeon.
        There are 6 mundane items and 2 magic items.
        The magic items have a probability associated with their rarity.
        """
        self.num_mundane = 6
        self.num_magic = 2
        self.num_high_rarity_chance = 0.1

        self.items = self.generate_items()

    def generate_items(self):
        """
        Generate the items for the shop.
        """

        magic_items = pd.read_csv('data/Items_magic.csv')
        mundane_items = pd.read_csv('data/Items.csv')

        # get the mundane items
        mundane_items = mundane_items.sample(self.num_mundane)
        mundane_items = mundane_items[["Name", "Value"]]

        # get the magic items
        magic_items = magic_items[["Name", "Rarity"]]

        # apply the cost to the magic items
        magic_items["Value"] = magic_items["Rarity"].apply(lambda x: MAGIC_ITEM_COST[x])

        # map the probability
        magic_items["Probability"] = magic_items["Rarity"].apply(lambda x: MAGIC_ITEM_RARITY[x])

        # sample the magic items based on the probability
        magic_items = magic_items.sample(self.num_magic, weights=magic_items["Probability"])

        magic_item_list = []
        for index, row in magic_items.iterrows():

            magic_item_list.append(row[['Name', 'Value']])
        
        mundane_item_list = []
        for index, row in mundane_items.iterrows():
            mundane_item_list.append(row[['Name', 'Value']])

        # combine the lists
        shop_items = mundane_item_list + magic_item_list

        return shop_items


