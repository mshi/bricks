# This file contains all the constants that will be used
# It contains colours and a bunch of other parameters

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Dimensions (in pixels)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BRICK_WIDTH = 45
BRICK_HEIGHT = 20
BRICK_SPACER = 2

BALL_RADIUS = 5

PLATFORM_WIDTH = 80
PLATFORM_HEIGHT = 20

# Number of brick slots available
GRID_WIDTH = 15
GRID_HEIGHT = 8
GRID_PADDING_X = (SCREEN_WIDTH - GRID_WIDTH * (BRICK_WIDTH + BRICK_SPACER)) / 2
GRID_PADDING_Y = (SCREEN_HEIGHT - GRID_HEIGHT * (BRICK_HEIGHT + BRICK_HEIGHT)) / 4

# Resource paths
IMAGE_BALL = "images/ball.png"
IMAGE_PLAYER = "images/platform.png"

BRICKS = [
    {
        "image": "images/bricks/grey.png",
        "health": -1,
        "points": 0
    },
    {
        "image": "images/bricks/cyan.png",
        "health": 1,
        "points": 10
    },
    {
        "image": "images/bricks/red.png",
        "health": 2,
        "points": 20
    },
    {
        "image": "images/bricks/green.png",
        "health": 3,
        "points": 40
    },
    {
        "image": "images/bricks/yellow.png",
        "health": 4,
        "points": 60
    },
    {
        "image": "images/bricks/blue.png",
        "health": 5,
        "points": 100
    },
]

MIN_BRICK_POWER = 0
MAX_BRICK_POWER = 5

BRICK_RANDOM_CHANCE = 10
BALL_DAMAGE = 1

# parameters
BALL_INITIAL_VELOCITY = 10  # velocity in pixels/refresh
BALL_INITIAL_DIRECTION = 0  # start at 0 degrees

PLAYER_SPEED = 10  # 10 pixels/refresh

VERSION = "1.0"
NAME = "BrickBreaker"
FPS = 60  # 60 frames per second

STATES = {
    "IDLE": 0,
    "STARTED": 1,
    "PAUSED": 2,
    "GAMEOVER": 3,
    "MENU": 4
}
