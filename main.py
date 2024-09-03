from dungeon_files.dungeon import *
from globals import *

import cProfile
import pstats

def main():
    # Create the dungeon.

    dungeon = Dungeon(depth=2, complexity=2, difficulty=2)
    profiler = cProfile.Profile()
    profiler.enable()
    dungeon.generate_dungeon()
    profiler.disable()
    dungeon.draw_dungeon()
    
    dungeon.display_rooms()
    

    stats = pstats.Stats(profiler).sort_stats('cumulative')
    # stats.print_stats(20)

if __name__ == "__main__":
    main()