# Description: This file contains global variables that are used throughout the program.


COLOURS = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'YELLOW': (255, 255, 0),
    'CYAN': (0, 255, 255),
    'MAGENTA': (255, 0, 255),
    'ORANGE': (255, 165, 0),
}

# dungeon settings
GENERAL_ROOM_TYPES = {
    "monster" : 0.3,
    "trap" : 0.3,
    "shop" : 0.2,
    "shrine" : 0.1
}


SPECIAL_ROOM_TYPES = [
    "boss",
    "vault"
]

ROOM_SIZES = {
    "SMALL" : (5,5),
    "MEDIUM" : (10,10),
    "LARGE" : (15,15),
    "HUGE" : (20,20),
    "GIGANTIC" : (25,25),  
}

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 640
CENTRE = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
TILE_SIZE = WINDOW_WIDTH // 32


FLOOR_COLOR = COLOURS['WHITE']
WALL_COLOR = COLOURS['BLACK']
EXIT_COLOR = COLOURS['RED']
ENTRANCE_COLOR = COLOURS['GREEN']   
TRAP_COLOR = COLOURS['ORANGE']

DISPLAY = (WINDOW_WIDTH, WINDOW_HEIGHT)