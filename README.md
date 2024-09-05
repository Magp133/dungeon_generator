
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

If the room is a trap it will look like the following:
![alt text](example_dungeon/dungeon_room2.png)

If the room type is 'trap' then the traps will be generated and placed within the room. Trap locations are determined by the entrance, exits and the center of the room. They are placed within a random spread around these locations to give variability and reduce predictibility. These wont be shown to the players and are a reference for the game master to use. 

Room types have a chance to appear. This is shown by the following dict used in the globals.  
GENERAL_ROOM_TYPES = {
    "monster" : 0.3,
    "trap" : 0.3,
    "shop" : 0.2,
    "shrine" : 0.1
}  
Boss and vault are not there as they are special rooms which must be added at the end. 
Extra rooms can be added but their functionality would also need to be added into the generate_features of the DungeonRoom. This shouldn't be difficult to do. A new class of room would be created and the details would be placed in there to return the required information to log into the dungeon log.

The entrances and exits between the rooms are placed randomly around the edges of the room without overlapping each other. The corridors between the rooms are not considered. I planned on having these dungeons act more like a roguelite game where the entraces/ exits are directly connected to one another. If feedback from this during playtesting changes then I will update this.

## Dungeon Logs.
The information within the dungeon is recorded into a text file representing each room and the contents within it. For the full log look into the example dungeon folder and read the file there. 

For monsters:

*Room 1*   
*Room Size: (5, 5)*  
*Room Type: monster*  
*Monsters: Constructed Commoner, Replica Tridrone, Homunculus, Crystal Battleaxe, Homunculus, Demos Magen, Strixhaven Campus Guide, Swarm of Mechanical Spiders, Stone Giant Statue, Animated Armor, Stone Giant Statue, Demos Magen,*  

For traps:

*Room 2*  
*Room Size: (10, 10)*  
*Room Type: trap*  
*Trap: Swinging Blade Trap*  
*A swinging blade trap is a large blade that swings down from the ceiling or up from the floor when triggered. The blade is usually razor-sharp and can cut through flesh and bone with ease.*  
*2d10 slashing damage*  
*Dexterity DC 15*  

*Trap: Swinging Blade Trap*  
*A swinging blade trap is a large blade that swings down from the ceiling or up from the floor when triggered. The blade is usually razor-sharp and can cut through flesh and bone with ease.*  
*2d10 slashing damage*  
*Dexterity DC 15*  

*Trap: Swinging Blade Trap*  
*A swinging blade trap is a large blade that swings down from the ceiling or up from the floor when triggered. The blade is usually razor-sharp and can cut through flesh and bone with ease.*  
*2d10 slashing damage*  
*Dexterity DC 15*  

*Trap: Poison Gas Trap*  
*A poison gas trap is a hidden mechanism that releases a cloud of poisonous gas when triggered. The gas is usually colorless and odorless, making it difficult to detect until it is too late.*  
*2d6 poison damage*  
*Constitution DC 15*  

For shops:

(this is from another dungeon. This example one didn't generate a shop)

*Room 1*   
*Room Size: (5, 5)*  
*Room Type: shop*  
*Shop Items: Lance: 10 gp, Bombard: 50,000 gp, Sleep Grenade: nan, Turtle Ship: 40,000 gp, Trinket: nan, Chicken: 2 cp, Claw of the Wyrm Rune: 4000, Potion of Heroism: 4000,*  

For bosses:

*Room 31*  
*Room Size: (10, 10)*  
*Room Type: boss*  
*Boss: Helmed Horror*  
*Minions: Constructed Commoner, Animated Broom,*  

For vaults:

*Room Size: (5, 5)*    
*Room Type: vault*     
*Gold: {'copper': 485, 'silver': 992, 'gold': 42, 'platinum': 9}*  
*Gems: {'worth': 825, 'type': 'Sardonyx'}*  
*Magic Items: ['Pixie Dust' 1500]*  

For shrines:
Shrines do not have any information as they are a custom thing I am adding for my own games. This will be updated later but isn't important for the actual dungeon as the goal was traps, monsters and treasure.


## Dungeon Data
As mentioned breifly at the start the monster information is from this site: https://5e.tools/bestiary.html#aarakocra_mm where I downloaded the entire database as a csv and filtered the columns. The CR (challenge rating) had to be converted into an int and the Type had to be cleaned as there were issues comparing it to strings.  

There was an issue with monsters not getting chosen for the dungeon. This was due to how some monster types and how boss generation works. Boss generation takes the dungeon difficulty and adds a random integer between 1 and 3 to it. It will then filter the monster database for a monsters with that CR and choose one. This defines the type of monsters that are allowed to be generated as mentioned before with type.  

The issue with this is that some monster types do not have many low CR monsters. Additionally the types are sometimes in the form of the following *Humanoid (Kobold)*. They have a subtype within their core type. These types as a whole may not meet the CR requirments either. To get around this if the monster db is empty after filtering and sampling the conditions are relaxed and only considers the core type which would be *Humanoid* in the previous example. 

If an error occurs due to this then it probably attempted to make a boss a dragon (one of the low CR ones) which doesn't have any low CR monsters. Though with the settings it had for this example dungeon it might just be in range for one or two of the lowest. Run it again and it should generate a fully functional dungeon.
