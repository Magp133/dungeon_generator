from pprint import pprint
import random
import numpy as np

class RoomTraps():
    def __init__(self, traps: list, room_map: list, trap_data: dict, difficulty: int) -> None:
        self.traps = traps # list of the traps in the room
        self.room_map = room_map # the room map

        self.occupied_tiles = set() # the tiles that are already occupied by traps.

        self.trap_info = dict() # the information about the traps in the room.

        self.max_search_tries = 100 # the maximum number of tries to find a location for the trap.

        self.trap_data = trap_data # the trap data

        self.difficulty = difficulty # the difficulty of the room.

        self.generate_trap()

    def generate_trap(self):
        """
        Generate a trap in the room.
        Use the room map to find the optimal location for the trap.
        Update the room map to reflect the trap.
        """

        # with open("data/traps.json", "r") as f:
        #     trap_data = json.load(f)

        for trap in self.traps:
            # Find the optimal location for the trap.
            trap_location = self.find_optimal_trap_location()
            
            if trap_location is None:
                continue
            # Add the trap location to the occupied tiles.
            self.occupied_tiles.add(trap_location)

            # Update the room map to reflect the trap.
            self.room_map[trap_location[1]][trap_location[0]] = -1

            # # Add the trap information to the trap info dictionary.
            self.trap_info[trap_location] = self.trap_data["traps"][trap]
        
        # pprint(self.room_map)

    def find_optimal_trap_location(self):
        """
        Uses the room map to find the optimal location for the trap.
        Does this by placing traps near the entrance and the exits of the room as well as near the centre. 
        """
        
        entrance, exits, centre = self.find_exits_entrances()

        # Find the optimal location for the trap.
        # The optimal location is near the  entrance, exits, and the centre of the room.
        # add to the viable trap locations by choosing traps within a certain distance of the entrace, exits
        # and near the centre of the room.

        viable_trap_locations = [entrance, centre] + list(exits)
        viable_trap_weights = [1, 3] + list(np.ones(len(list(exits))))

        spread = 4

        for _ in range(self.max_search_tries):
            #use the weights and the locations to choose a location
            cluster_choice = random.choices(viable_trap_locations, weights=viable_trap_weights)[0]

            # print(cluster_choice)

            # add some randomness to the trap location around the cluster choice
            # ensuring that the trap is not placed on the entrance or exits
            # and that the trap is not placed on the same location as another trap.
            # addionally, the trap should be placed on a walkable tile.

            if cluster_choice[0] == 0: # if the cluster choice is on the left edge of the room.
                x = random.randint(1, spread)
                cluster_choice = (cluster_choice[0] + x, cluster_choice[1])
            
            if cluster_choice[0] == len(self.room_map[0]) - 1: # if the cluster choice is on the right edge of the room.
                x = random.randint(1, spread)
                cluster_choice = (cluster_choice[0] - x, cluster_choice[1])

            if cluster_choice[1] == 0: # if the cluster choice is on the top edge of the room.
                y = random.randint(1, spread)
                cluster_choice = (cluster_choice[0], cluster_choice[1] + y)
            
            if cluster_choice[1] == len(self.room_map) - 1: # if the cluster choice is on the bottom edge of the room.
                y = random.randint(1, spread)
                cluster_choice = (cluster_choice[0], cluster_choice[1] - y)
            
            # Check if the location is unoccupied and within the room boundaries
            if cluster_choice not in self.occupied_tiles:
                return cluster_choice
    
    def check_location(self, location):
        """
        Check if the location is already occupied by another trap.
        """
        return self.room_map[location[1]][location[0]] == "T"

    
    def find_exits_entrances(self):
        """
        locate the entrances and exits within the room.
        """
        # find the centre of the room
        room_width = len(self.room_map[0])
        room_height = len(self.room_map)
        centre = (room_width // 2, room_height // 2)

        entrance = None
        exits = set()

        # find the entrance and exits of the room
        # the entrances/ exits are around the edge of the room
        #exits are 2
        #entrance is 1
        for i in range(room_width - 1):
            if self.room_map[0][i] == 2 and (i,0) not in exits: # exit on the top row.
                exits.add((i, 0))
            if self.room_map[room_height - 1][i] == 2 and (i, room_height - 1) not in exits: # exit on the bottom row.
                exits.add((i, room_height - 1))

            if self.room_map[0][i] == 3: # entrance on the top row.
                entrance = (i, 0)
            if self.room_map[room_height - 1][i] == 3: # entrance on the bottom row.
                entrance = (i, room_height - 1) 

        for i in range(room_height - 1):
            if self.room_map[i][0] == 2 and (0,1) not in exits: # exit on the left column.
                exits.add((0, i))
            if self.room_map[i][room_width - 1] == 2 and (room_width - 1, i) not in exits: # exit on the right column.
                exits.add((room_width - 1, i)) 

            if self.room_map[i][0] == 3: # entrance on the left column.
                entrance = (0, i)
            if self.room_map[i][room_width - 1] == 3:
                entrance = (room_width - 1, i)
        
        # Explicitly check the bottom right corner
        if self.room_map[room_height - 1][room_width - 1] == 2:
            exits.add((room_width - 1, room_height - 1))
        if self.room_map[room_height - 1][room_width - 1] == 3:
            entrance = (room_width - 1, room_height - 1)

        return entrance, exits, centre