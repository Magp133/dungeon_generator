
I have made this as a map generator for the table top game Dungeons and Dragons.
This generates a planar drawing of a graph map in bokeh. 
Rooms are generated from the nodes within the graph and assigned types: monster, trap, shrine, boss, vault, shop.
Traps are generated from within the trap room where the data is from the traps.json file.
Monsters are generated within the monster room where the data is from the bestiary.csv file. This was downloaded from this site: https://5e.tools/bestiary.html#aarakocra_mm

# Example Generation.
## Graph generation.
![alt text](example_dungeon/dungeon_graph.png)
This graph is first generated. Each node is assigned a room type from global variables. This is used when generating the room maps and information. Node generation is done by determining how many children each node should have. This is done by having a random integer chosen between 1 and the complexity of the dungeon. The depth determines when the iteration of the node generation finishes. 

Once the graph hits the nodes at the max depth a boss room will attempt to spawn as the final node. If this is successful a vault room will be created immediately after the boss with only one connection to the boss. This marks the last step in generating the initial graph. 

The next step is to add extra edges between nodes/ rooms. This creates a more natural feeling dungeon as well as adding some paths between the trees avoiding having to run all the way back up to explore a different branch. A node is not allowed to connect to the another room if it is a vault. This is to force having to encounter the boss before getting into the vault to make the dungeon more challenging and interesting.

The graph is fully done. This will be the layout for the dungeon. Rooms will now be generated.

## Room generation.
### Initial generation.
Just before rooms are generated, defining who the boss of the dungeon will make the dungeon easier to create. This enables that the monsters and, if required, the traps to have a theme depending upon the boss. For example, if the the boss is an undead create then only undead monsters will be added to the dungeon giving an undead theme. 

### Room initialisation.
Room generation begins by creating a DungeonRoom for each node. Each room has the following information: 
- size: how large the room is. Defined in the globals. Chosen depending on the difficulty of the dungeon. Higher difficulty -> bigger rooms.
- neighbours: used to create the entrance and exits within the map.
- difficulty: used to determine the challenge rating of monsters.
- room_type: entrance, shop, boss, vault, monster, trap, shrine.
- boss of the dungeon: defined for creating monsters and themes within the room. 

### Room creation.
A room will look like the following:
![alt text](example_dungeon/dungeon_room0.png)