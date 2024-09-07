"""
Created by: Evan Richards-Ward
Date: 7/9/2024
"""


import random
import pandas as pd

from globals import *

class RoomVault():
    def __init__(self, difficulty: int) -> None:
        """
        Init the vault.
        The vault will have gold, gems and magic items. 
        """

        self.difficulty = difficulty

        self.gold = self.generate_gold()
        self.gems = self.generate_gems()
        self.magic_items = self.generate_magic_items()
    
    def generate_gold(self):
        """
        Generates the gold for the vault.
        copper, silver, gold, platinum can be generated.
        """
            
        gold_reward = {
            'copper': random.randint(1, 1000),
            'silver': random.randint(1, 1000),
            'gold': random.randint(1, 100),
            'platinum': random.randint(1, 10)
        }

        return gold_reward

    def generate_gems(self):
        """
        Generates the gems for the vault.
        Gems with a worth and type
        """

        gems = {
            'worth': random.randint(1, 1000),
            'type': random.choice(GEM_TYPES)
        }

        return gems


    def generate_magic_items(self):
        """
        Generates the magic items for the vault.
        """

        magic_items = pd.read_csv('data/Items_magic.csv')
        magic_items = magic_items[["Name", "Rarity"]]

        # apply the cost to the magic items
        magic_items["Value"] = magic_items["Rarity"].apply(lambda x: MAGIC_ITEM_COST[x])

        # map the probability
        magic_items["Probability"] = magic_items["Rarity"].apply(lambda x: MAGIC_ITEM_RARITY[x])

        # remove the unknown and varies
        # remove the common
        magic_items = magic_items[magic_items["Rarity"] != 'common']
        magic_items = magic_items[magic_items["Rarity"] != 'unknown (magic)']
        magic_items = magic_items[magic_items["Rarity"] != 'varies']

        # take one magic item
        magic_item = magic_items.sample(weights=magic_items["Probability"])


        return magic_item[['Name', 'Value']].values[0]
