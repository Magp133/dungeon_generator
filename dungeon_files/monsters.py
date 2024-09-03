import random
import pandas as pd
from pprint import pprint

class RoomMonsters():
    def __init__(self, boss_monster_type: str, difficulty: int) -> None:
        """
        Defines the monsters within the room. 
        Monsters are chosen from the database based on the difficulty of the room,
        as well as the type of boss that oversees the dungeon. 
        """

        self.boss_monster_type = boss_monster_type
        self.difficulty = difficulty

        self.monster_list = self.generate_monsters()

    def generate_monsters(self):
        """
        Generates monsters based on type and CR (difficulty).
        """

        # filter for two conditions.
        # 1. The monster must be of the same type as the boss.
        # 2. The monster must be within the difficulty range of the room.

        # Step 1: Read the CSV file into a pandas DataFrame
        df = pd.read_csv('data/Bestiary.csv')

        # filter for the boss type
        df = df[df['Type'].str.contains(self.boss_monster_type, na=False)]

        # filter for the difficulty
        df = df[df['CR'] <= self.difficulty]


        if df.empty:
            print("No monsters found.")
            return None

        # Step 3: Randomly select a monster from the filtered DataFrame.
        # 4 monsters of the self.difficulty level can be chosen. 
        # For each level of difficulty, the number of monsters increases by 1.
        # For example, if the difficulty is 2, 4 monsters of CR 2 can be chosen.
        # and if the difficulty is 2, then 8 monsters of CR 1 can be chosen.
        monster_list = []
        monster_points = 4 * self.difficulty

        while monster_points > 0:
            monster = df.sample()
            monster_points -= monster['CR'].values[0]
            monster_list.append(monster)

        return monster_list

class RoomBoss():
    def __init__(self, difficulty: int, type: str) -> None:
        """
        Defines the boss of the room. 
        The boss is chosen from the database based on the difficulty of the room.
        """

        self.difficulty = difficulty
        self.boss_type = type  

        self.minions = self.generate_boss_room()

    def generate_boss_room(self):
        """
        Generates the minions for the boss of the room based on the difficulty.
        """



        # Step 1: Read the CSV file into a pandas DataFrame
        df = pd.read_csv('data/Bestiary.csv')

        # filter for the boss type
        df = df[df['Type'].str.contains(self.boss_type, na=False)]

        # filter for the difficulty
        df = df[df['CR'] == self.difficulty]


        if df.empty:
            print("No monsters found.")
            return None

        num_minions = random.randint(1, self.difficulty)
        minions = []

        for i in range(num_minions):
            minion = df.sample()
            minions.append(minion)

        return minions
