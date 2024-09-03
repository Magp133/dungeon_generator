"""
Defines the class for the dungeon.
Defines the class for the dungeon room.
Will include encounters, items and traps which can be rolled from the event handler.
"""
from globals import *

#dungeon stuff
import networkx as nx
import random
from bokeh.plotting import figure, show
from bokeh.models import GraphRenderer, StaticLayoutProvider, Circle, LabelSet, ColumnDataSource
from bokeh.io import output_notebook
import networkx as nx
import os

#room stuff
from .dungeon_room import *

import pandas as pd

class Dungeon:
    def __init__(self, depth: int, complexity: int, difficulty: int) -> None:
        """
        depth indicates how many rooms max must be traversed before the final boss room.
        size generates the grid of the dungeon. how spread out the dungeon is. 
        complexity indicates how many branches a room can have in a dungeon. 
        """
        self.dungeon_map = nx.DiGraph() # Dungeon map
        self.dungeon_rooms = {} # Dungeon rooms
 
        self.depth = depth # Depth of the dungeon
        self.complexity = complexity # Complexity of the dungeon
        self.difficulty = difficulty # Difficulty of the dungeon

        # create a text file containing the dungeon info. 
        # the dungeon info format is as follows:
        # room ID, room type
        # traps, monsters and items in the room. Each starting on a new line. 
        with open('dungeon_info.txt', 'w') as file:
            file.write("Dungeon Info\n")
    
    def generate_dungeon(self):
        """
        Generates the dungeon.
        """
        self.generate_level(0)
        self.generate_extra_edges()
        self.boss = self.generate_boss()
        self.generate_rooms()
        return self.dungeon_map

    def generate_level(self, root_node: int):
        """
        Generates the level of the dungeon.
        This version of the function works up to complexity 8 at depth 3 where it breaks due to the graph not being planar. 
        """
        stack = [(root_node, 0)] # (node, level)

        room_types = list(GENERAL_ROOM_TYPES.keys())
        room_weights = list(GENERAL_ROOM_TYPES.values())
        boss_rooms = SPECIAL_ROOM_TYPES
        boss_chance = 0.3
        has_boss = False

        # add the first node to the dungeon.
        dungeon_info = {
            "type" : "entrance",
            "size" : self.choose_room_size(),
        }
        self.dungeon_map.add_node(0, dungeon_info=dungeon_info)

        while stack:
            node, level = stack.pop()

            # base case
            # the final rooms/ depest parts of the dungeon.
            if level == self.depth:
                #create the room info
                if random.random() < boss_chance and not has_boss:
                    room_type = boss_rooms[0]
                    has_boss = True
                else:
                    room_type = random.choice(room_types)
                    boss_chance += 0.1

                dungeon_info = {
                    "type" : room_type,
                    "size" : random.choice(list(ROOM_SIZES.keys())),
                }
                
                # code for adding a boss room to the dungeon.
                if room_type == "boss":
                    child_node = node * 10 + 1
                    # add the boss node to the dungeon.
                    self.dungeon_map.add_node(node, dungeon_info=dungeon_info)
                    
                    # add the vault node to the dungeon.
                    self.dungeon_map.add_node(child_node, dungeon_info={"type" : boss_rooms[1], "size" : random.choice(list(ROOM_SIZES.keys()))})
                    self.dungeon_map.add_edge(node, child_node)


            else:
                #try and stop long chains of a single room in a more complex dungeon.
                if level > self.depth / 2:
                    num_children = random.randint(0, self.complexity)
                else:
                    num_children = random.randint(1, self.complexity)

                # create new children and add them to the stack. 
                for child in range(1, num_children + 2):
                    
                    child_node = node * 10 + child

                    #create the room info
                    room_type = random.choices(room_types, room_weights)[0]

                    # if the room type is a shop roll again and remove the shop from the list if it succeeds again.
                    # this is intended to allow the shop to spawn later and only once instead of lots or near the start. 
                    if room_type == "shop":
                        room_types.remove("shop")
                        room_weights.remove(GENERAL_ROOM_TYPES["shop"])

                    dungeon_info = {
                        "type" : room_type,
                        "size" : random.choice(list(ROOM_SIZES.keys())),
                    }

                    self.dungeon_map.add_node(child_node, dungeon_info=dungeon_info)
                    self.dungeon_map.add_edge(node, child_node)

                    #append the child to the stack.
                    stack.append((child_node, level + 1))



    def generate_extra_edges(self):
        """
        Generate extra edges for the dungeon.
        """
        for _ in range(self.complexity):
            node1, node2 = random.sample(list(self.dungeon_map.nodes), 2)

            #check if the nodes are already connected.
            # additionally, check if the nodes are a vault. if so do not connect them.
            if not self.dungeon_map.has_edge(node1, node2) and not self.dungeon_map.nodes[node1]['dungeon_info']['type'] == "vault" and not self.dungeon_map.nodes[node2]['dungeon_info']['type'] == "vault":
                self.dungeon_map.add_edge(node1, node2)
                self.dungeon_map.add_edge(node2, node1)

    def generate_boss(self):
        """
        Generates the boss monster of the dungeon to use for the final room.
        """
        monsters = pd.read_csv("data/Bestiary.csv")
        monster_cr = self.difficulty + random.randint(1, 3)
        boss_candidates = monsters[monsters['CR'] == monster_cr]
        boss = boss_candidates.sample()
        return boss
        

    def generate_rooms(self):
        """
        Generates the rooms depending on the type of room it is. 
        """
        nodes = list(self.dungeon_map.nodes)

        for node in nodes:
            room_info = self.dungeon_map.nodes[node]['dungeon_info']
            size = self.choose_room_size()
            # get the neighours of the node
            neighbours = nx.neighbors(self.dungeon_map, node)

            # remove the parent node from the neighbours
            neighbours = list(neighbours)
            if node // 10 in neighbours:
                neighbours.remove(node // 10)

            with open('dungeon_info.txt', 'a') as file:
                file.write("\n")
                file.write(f"Room {node}\n")

            #create the room
            room = DungeonRoom(size=size, neighbours=neighbours, difficulty=self.difficulty, type=room_info['type'], boss=self.boss)

            #add the room to the dungeon rooms
            self.dungeon_rooms[node] = room

            #add the room to the dungeon info file
            

    def choose_room_size(self):
        """
        Chooses the size of the room.
        the selection depends on the difficulty of the dungeon.
        """
        room_sizes = list(ROOM_SIZES.values())

        if self.difficulty == 1:
            return random.choice(room_sizes[:2])
        elif self.difficulty == 2:
            return random.choice(room_sizes[:3])
        elif self.difficulty == 3:
            return random.choice(room_sizes[:4])
        elif self.difficulty == 4:
            return random.choice(room_sizes[1:])
        else:
            return random.choice(room_sizes)

    def draw_dungeon(self):
        """
        Draws the dungeon.
        """
        plot = figure(title="Dungeon Layout", x_axis_label='X', y_axis_label='Y', x_range=(-1.1,2), y_range=(-1.1,2))
        graph_renderer = GraphRenderer()

        # Create a layout for the graph
        pos = nx.planar_layout(self.dungeon_map)
        graph_renderer.layout_provider = StaticLayoutProvider(graph_layout=pos)

        # Extract x and y coordinates from pos
        x, y = zip(*pos.values())

        # Add nodes and edges to the renderer
        graph_renderer.node_renderer.data_source.add(list(self.dungeon_map.nodes), 'index')
        graph_renderer.node_renderer.data_source.add(x, 'x')
        graph_renderer.node_renderer.data_source.add(y, 'y')
        graph_renderer.node_renderer.glyph = Circle(size=20, fill_color='white')
        graph_renderer.edge_renderer.data_source.data = dict(start=[e[0] for e in self.dungeon_map.edges], end=[e[1] for e in self.dungeon_map.edges])

        # Add labels to the nodes
        node_labels = list(self.dungeon_map.nodes)
        source = ColumnDataSource({'x': x, 'y': y, 'name': node_labels})
        labels = LabelSet(x='x', y='y', text='name', source=source, text_align='center', text_baseline='middle', text_color='black', text_font_size='10pt')

        plot.renderers.append(graph_renderer)
        plot.add_layout(labels)

        show(plot)


    
    def display_rooms(self):
        """
        Displays the rooms using pygame. 
        Once the room is created and displayed it will be saved before moving to the next room.
        """

        #delete everything in the room_images folder
        folder = 'room_images'
        for file in os.listdir(folder):
            os.remove(os.path.join(folder, file))
        

        # draw the rooms
        for node in self.dungeon_map.nodes.keys():
            # Create the screen
            screen = pg.display.set_mode(DISPLAY)
            screen.fill(pg.Color('black'))
            clock = pg.time.Clock()
            room = self.dungeon_rooms[node]
            room.draw_room(screen)
            pg.display.flip()
            clock.tick(60)


            # save the rooms
            filename = f"room_images/dungeon_room{node}.png"
            pg.image.save(screen, filename)
            pg.quit()
        


