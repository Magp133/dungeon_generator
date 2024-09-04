import pygame as pg

from pprint import pprint
import json
import numpy as np
from globals import *

#trap stuff
from .traps import *

# monster stuff
from .monsters import *

# shop stuff
from .shop import *

class DungeonRoom:
    def __init__(self, size: tuple, neighbours: list, difficulty: int, type: str, boss) -> None:
        """
        size indicates how big the room is. 
        encounters indicates the encounters within the room.
        items indicates the items within the room.
        traps indicates the traps within the room.
        """

        self.boss = boss

        self.size = size # (width, height)
        self.exit_list = neighbours
        self.exit_coord_name_pair = dict()
        self.type = type

        #dungeon info file
        with open('dungeon_info.txt', 'a') as file:
            file.write(f"Room Size: {self.size}\n")
            file.write(f"Room Type: {self.type}\n")
            # file.write("\n")
        
        #difficulty of the room
        self.difficulty = difficulty
        
        # generate the room map
        self.room_map = self.generate_room()
        self.generate_features()

        
        
    def generate_exits(self, exit):
        """
        Generates the exits for the room.
        """
        #generate a random exit coord
        #if it is not in the exit_coords list, add it to the list.
        while True:
            
            # choose where the exit will be and what var, x or y will be 0 or the max value.
            const = random.choice(['x', 'y'])

            if const == 'y':
                x = random.randint(0, self.size[0])
                y = random.choice([0, self.size[1]])
            if const == 'x':
                y = random.randint(0, self.size[1])
                x = random.choice([0, self.size[0]])

            if (x, y) not in self.exit_coord_name_pair.keys():
                self.exit_coord_name_pair[(x,y)] = exit
                return x, y

    def generate_room(self):
        """
        Generates a square room.
        """
        # print(f"Generating room of size {self.size}")
        room = np.zeros((self.size[0] + 1, self.size[1] + 1), dtype=int)

        for y in range(len(room)):
            for x in range(len(room[0])):
                if x == 0 or x == len(room[0]) - 1:
                    room[y][x] = 1
                if y == 0 or y == len(room) - 1:
                    room[y][x] = 1

        #generate the exits
        for exit in self.exit_list:
            x, y = self.generate_exits(exit)
            room[y][x] = 2

        #generate entrance
        x, y = self.generate_exits('Entrance')
        room[y][x] = 3

        return room
    
    def generate_features(self):
        """
        Generates the features of the room.
        This includes traps, enemies and items.
        """
        if self.type == "trap":
            self.traps = self.generate_traps()
        if self.type == "monster":
            self.monsters = self.generate_monsters()
        if self.type == "boss":
            self.boss = self.generate_boss()
        if self.type == "shop":
            self.shop = self.generate_shop()

    def generate_traps(self):
        """
        Generates traps within a room using a total cost of the level + difficulty to determine the level and amount of traps.
        """

        # calc the trap ratio based on the size of the room and the difficulty.
        trap_ratio = self.difficulty * (self.size[0] / 5)

        # print(f"Trap ratio: {trap_ratio}")
        #load the trap data
        with open('data/traps.json', 'r') as file:
            trap_data = json.load(file)
        
        trap_types = list(trap_data["traps"].keys())
        trap_costs = trap_data["costs"]

        #generate the traps
        traps = []
        while trap_ratio > 0:
            trap_type = random.choice(trap_types)
            trap_cost = trap_costs[str(trap_type)]
            if trap_ratio >= trap_cost:
                traps.append(trap_type)
                trap_ratio -= trap_cost
            else:
                trap_ratio = 0
            
        traps = RoomTraps(traps, self.room_map, trap_data, self.difficulty)

        # add the trap info to the dungeon info file
        with open('dungeon_info.txt', 'a') as file:

            for trap in traps.trap_info.values():
                # add each info to the dungeon info file
                file.write(f"Trap: {trap['name']}\n")
                file.write(f"{trap['description']}\n")
                file.write(f"{trap['damage']}\n")
                file.write(f"{trap['save']}\n")
                file.write("\n")

        return traps
    
    def generate_monsters(self):
        """
        Generate the monsters within the room.
        """
        boss_monster_type = self.boss['Type'].astype(str).values[0]
        monsters = RoomMonsters(boss_monster_type=boss_monster_type, difficulty=self.difficulty)

        # add the info to the dungeon info file
        with open('dungeon_info.txt', 'a') as file:
            file.write(f"Monsters: ")
            for monster in monsters.monster_list:
                file.write(f"{monster['Name'].values[0]}, ")
            file.write("\n")

        return monsters

    def generate_boss(self):
        """
        Add the boss to the dungeon and choose some helpers. 
        """
        minions = RoomBoss(difficulty=self.difficulty, type=self.boss['Type'].astype(str).values[0])

        # add the info to the dungeon info file
        with open('dungeon_info.txt', 'a') as file:
            file.write(f"Boss: {self.boss['Name'].values[0]}\n")
            file.write(f"Minions: ")
            for minion in minions.minions:
                file.write(f"{minion['Name'].values[0]}, ")
            file.write("\n")

        return minions

    def generate_shop(self):
        """
        Generates the items within the shop.
        Includes the price of the items.
        """
        shop = RoomShop()

        # add the info to the dungeon info file
        with open('dungeon_info.txt', 'a') as file:
            file.write(f"Shop Items: ")
            for item in shop.items:
                file.write(f"{item['Name']}: {item['Value']}, ")
            file.write("\n")

        return 


    def draw_room(self, screen):
        """
        Draws the room on the screen.
        The key for the room map values is as follows:
        - 0: floor
        - 1: wall
        - 2: exit
        - 3: entrance
       """

        #scaling factor to fit the room in the window
        scale_x = WINDOW_WIDTH / len(self.room_map[0]) 
        scale_y = WINDOW_HEIGHT / len(self.room_map)
        scale_factor = min(scale_x, scale_y)

        #centering the room in the window
        offset_x = (WINDOW_WIDTH - len(self.room_map[0]) * scale_factor) / 2
        offset_y = (WINDOW_HEIGHT - len(self.room_map) * scale_factor) / 2

        # iterate over the room map and draw the room
        for y in range(len(self.room_map)):
            for x in range(len(self.room_map[0])):
                # draw the floor
                if self.room_map[y][x] == 0:
                    pg.draw.rect(screen, FLOOR_COLOR, (x * scale_factor + offset_x, y * scale_factor + offset_y, scale_factor, scale_factor), 1)

                # draw the walls
                elif self.room_map[y][x] == 1:
                    pg.draw.rect(screen, WALL_COLOR, (x * scale_factor + offset_x, y * scale_factor + offset_y, scale_factor, scale_factor))

                # draw the exits
                elif self.room_map[y][x] == 2:
                    pg.draw.rect(screen, EXIT_COLOR, (x * scale_factor + offset_x, y * scale_factor + offset_y, scale_factor, scale_factor))

                    #draw the exit name
                    pg.font.init()
                    font_size = int(scale_factor / 2)
                    font = pg.font.SysFont('Comic Sans MS', font_size)
                    text = font.render(str(self.exit_coord_name_pair[(x,y)]), True, COLOURS['BLACK'])
                    screen.blit(text, (x * scale_factor + offset_x, y * scale_factor + offset_y))

                # draw the entrance
                elif self.room_map[y][x] == 3:
                    pg.draw.rect(screen, ENTRANCE_COLOR, (x * scale_factor + offset_x, y * scale_factor + offset_y, scale_factor, scale_factor))

                    #draw the entrance name
                    pg.font.init()
                    font_size = int(scale_factor / 5)
                    font = pg.font.SysFont('Comic Sans MS', font_size)
                    text = font.render(str(self.exit_coord_name_pair[(x,y)]), True, COLOURS['BLACK'])
                    screen.blit(text, (x * scale_factor + offset_x, y * scale_factor + offset_y))

                # draw the traps
                elif self.room_map[y][x] == -1:
                    pg.draw.rect(screen, TRAP_COLOR, (x * scale_factor + offset_x, y * scale_factor + offset_y, scale_factor, scale_factor))

                    # draw the trap name
                    pg.font.init()
                    name = self.traps.trap_info[(x,y)]['name']


                    #scale the font_size based on the name length such that it fits in the tile.
                    font_size = int(scale_factor / (len(name) / 2))


                    # font_size = int(scale_factor / 6)
                    font = pg.font.SysFont('Comic Sans MS', font_size)


                    text = font.render(name, True, COLOURS['BLACK'])
                    screen.blit(text, (x * scale_factor + offset_x, y * scale_factor + offset_y))