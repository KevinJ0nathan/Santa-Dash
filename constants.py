import pygame
import math
#Initializes pygame
pygame.init()
pygame.mixer.init()
score_sound = pygame.mixer.Sound('game_sounds/score.wav')
score_sound.set_volume(0.3)
# The window width and height
screen_width = 900
screen_height = 950
# Intialize the font
font = pygame.font.Font('freesansbold.ttf', 20)
# Load custom icon image
icon_image = pygame.image.load('icon.png')
# Makes an empty list to store images of player
player_images = []
# Iterates over all the images in the folder and put it in the list
for i in range(1, 5):
            player_images.append(pygame.transform.scale(pygame.image.load(f'character_images/{i}.png'), (50, 50)))
# Create a Pygame clock object to control the frame rate
timer = pygame.time.Clock()
# Sets the fps to 60
fps = 60
# Initialize the counter
counter = 0  
MAX_COUNTER = 19
# Initialize the game window and caption
screen = pygame.display.set_mode((screen_width, screen_height))
# Stores the value of pi in a variable
PI = math.pi


# Constants for the map
EMPTY = 0
PRESENT = 1
CANDY = 2
VERTICAL_LINE = 3
HORIZONTAL_LINE = 4
TOP_RIGHT = 5
TOP_LEFT = 6
BOTTOM_LEFT = 7
BOTTOM_RIGHT = 8


# Directions
RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3
direction_command = RIGHT

# Score
score = 0
highscore = 0
#Score position
score_position = (10,920)
#highscore position
highscore_position = (150,920)

# Powerup 
powerUp = False
# Powerup counter
power_counter = 0
# Maximum duration for powerup
MAX_POWER_DURATION = 200
MAX_DEBUFF_DURATION = 200
STARTUP_DURATION = 180

#Lives
lives = 3


PLAYER_LIVES_SIZE = (30,30)
PLAYER_LIVES_START_POS_X = 650
PLAYER_LIVES_START_POS_Y = 915
PLAYER_LIVES_GAP = 40

#Offset variables
OFFSET_X = 23
OFFSET_Y = 24
OFFSET_ENEMY = 22


# Constants for boundaries, reset values, and movement offset
RIGHT_BOUNDARY = 900
LEFT_BOUNDARY = -50
RESET_RIGHT = -47
RESET_LEFT = 897
MOVEMENT_OFFSET = 20

startup_counter = 0

# Constants for calculation
row_spacing = (screen_height - 50) // 32
column_spacing = screen_width // 30
fudge_factor = 15

x_pos = 0
y_pos = 1

# Define starting positions
START_PLAYER_X = 430
START_PLAYER_Y = 550
START_EVIL_SNOWMAN_X = 84
START_EVIL_SNOWMAN_Y = 70
START_ICE_SPIRIT_X = 776
START_ICE_SPIRIT_Y = 70
START_THIEF_X = 84
START_THIEF_Y = 800

evilSnowman_images = pygame.transform.scale(pygame.image.load(f'enemy_images/Snowman.png'), (45, 45))
evilSnowman_position_x = 84
evilSnowman_position_y = 70
evilSnowman_direction = RIGHT
evilSnowman_speed = 2

iceSpirit_images = pygame.transform.scale(pygame.image.load(f'enemy_images/icespirit.png'), (45, 45))
iceSpirit_position_x = 776
iceSpirit_position_y = 70
iceSpirit_direction = RIGHT
iceSpirit_speed = 2

thief_images = pygame.transform.scale(pygame.image.load(f'enemy_images/thief.png'), (45, 45))
thief_position_x = 84
thief_position_y = 800
thief_direction = RIGHT
thief_speed = 2

# Modified speed for powerup
modified_evilSnowman_speed = 2
modified_iceSpirit_speed = 2
modified_thief_speed = 2

game_over = False
game_won = False

debuff = False
debuff_timer = 0

victory_image = pygame.image.load('Victory.png')
victory_image = pygame.transform.scale(victory_image, (screen_width, screen_height))

game_over_image = pygame.image.load('Gameover.png')
game_over_image = pygame.transform.scale(game_over_image, (screen_width, screen_height))

# Define penalty constants
LIVES_PENALTY = 1
SCORE_PENALTY = 10
