# game options/settings
TITLE = "Flapper!"
WIDTH = 800
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial'
HS_FILE = 'highscore.txt'
SPRITESHEET = 'flapper_sprites.png'
VOLUME = 0.05

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 15

# Pipe properties
FLOOR_HEIGHT = 40
PIPE_WIDTH = 54 # 60
PIPE_GAP = 200
PIPE_BUFFER = 25
PIPE_SPREAD = 400
PIPE_HEIGHT = 322

# Starting platforms
"""PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
                 (WIDTH, 0, PIPE_WIDTH, PIPE_BUFFER + 250),
                 (WIDTH, 250 + PIPE_GAP + PIPE_BUFFER, PIPE_WIDTH, HEIGHT - (250 + PIPE_BUFFER)),
                 (WIDTH + PIPE_SPREAD, 0, PIPE_WIDTH, PIPE_BUFFER + 50),
                 (WIDTH + PIPE_SPREAD, 50 + PIPE_GAP + PIPE_BUFFER, PIPE_WIDTH, HEIGHT - (50 + PIPE_BUFFER)),
                 (WIDTH + 2 * PIPE_SPREAD, 0, PIPE_WIDTH, PIPE_BUFFER + 300),
                 (WIDTH + 2 * PIPE_SPREAD, 300 + PIPE_GAP + PIPE_BUFFER, PIPE_WIDTH, HEIGHT - (300 + PIPE_BUFFER))
                 ]"""

PLATFORM_LIST = [(WIDTH, 100),
                (WIDTH + PIPE_SPREAD, 200),
                (WIDTH + 2*PIPE_SPREAD, 300)
                ]

FLOOR_POS = (0, HEIGHT - 40)
FLOOR_DIMS = (WIDTH, 40)

"""FLOOR_POS = (PLATFORM_LIST[0][0], PLATFORM_LIST[0][1])
FLOOR_DIMS = (PLATFORM_LIST[0][2], PLATFORM_LIST[0][3])"""

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE
