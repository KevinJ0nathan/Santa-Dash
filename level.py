import pygame
from constants import *
import copy

boards = [
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,6,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,5,0],
[0,3,6,4,4,4,4,4,4,4,4,4,4,4,5,6,4,4,4,4,4,4,4,4,4,4,4,5,3,0],
[0,3,3,2,1,1,1,1,1,1,1,1,1,1,3,3,1,1,1,1,1,1,1,1,1,1,2,3,3,0],
[0,3,3,1,6,5,1,6,5,1,6,4,5,1,3,3,1,6,4,5,1,6,5,1,6,5,1,3,3,0],
[0,3,3,1,3,3,1,3,3,1,3,0,3,1,3,3,1,3,0,3,1,3,3,1,3,3,1,3,3,0],
[0,3,3,1,3,3,1,3,3,1,3,0,3,1,3,3,1,3,0,3,1,3,3,1,3,3,1,3,3,0],
[0,3,3,1,7,8,1,7,8,1,7,4,8,1,7,8,1,7,4,8,1,7,8,1,7,8,1,3,3,0],
[0,3,3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,3,0],
[0,3,3,1,6,4,4,5,1,6,5,1,6,4,4,4,4,5,1,6,5,1,6,4,4,5,1,3,3,0],
[0,3,3,1,7,4,4,8,1,3,3,1,7,4,5,6,4,8,1,3,3,1,7,4,4,8,1,3,3,0],
[0,3,3,1,1,1,1,1,1,3,3,1,1,1,3,3,1,1,1,3,3,1,1,1,1,1,1,3,3,0],
[0,3,3,1,6,4,4,4,4,8,7,4,5,1,3,3,1,6,4,8,7,4,4,4,4,5,1,3,3,0],
[0,3,3,1,7,4,4,4,4,5,6,4,8,1,7,8,1,7,4,5,6,4,4,4,4,8,1,3,3,0],
[0,3,3,1,1,1,1,1,1,3,3,1,1,1,1,1,1,1,1,3,3,1,1,1,1,1,1,3,3,0],
[4,8,7,4,4,4,4,5,1,3,3,1,6,4,4,4,4,5,1,3,3,1,6,4,4,4,4,8,7,4],
[0,0,0,0,0,0,0,3,1,7,8,1,7,4,4,4,4,8,1,7,8,1,3,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,0,0,0,0,0,0,0],
[4,4,4,4,4,4,4,8,1,6,5,1,6,4,4,4,4,5,1,6,5,1,7,4,4,4,4,4,4,4],
[0,0,0,0,0,0,0,0,1,3,3,1,7,4,4,4,4,8,1,3,3,1,0,0,0,0,0,0,0,0],
[4,4,4,4,4,4,4,5,1,3,3,1,1,1,1,1,1,1,1,3,3,1,6,4,4,4,4,4,4,4],
[0,0,0,0,0,0,0,3,1,3,7,4,5,1,6,5,1,6,4,8,3,1,3,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,3,1,3,6,4,8,1,7,8,1,7,4,5,3,1,3,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,3,1,3,3,1,1,1,1,1,1,1,1,3,3,1,3,0,0,0,0,0,0,0],
[4,5,6,4,4,4,4,8,1,7,8,1,6,4,4,4,4,5,1,7,8,1,7,4,4,4,4,5,6,4],
[0,3,3,1,1,1,1,1,1,1,1,1,3,0,0,0,0,3,1,1,1,1,1,1,1,1,1,3,3,0],
[0,3,3,1,6,4,4,4,4,4,5,1,3,0,0,0,0,3,1,6,4,4,4,4,4,5,1,3,3,0],
[0,3,3,1,3,0,0,0,0,0,3,1,3,0,0,0,0,3,1,3,0,0,0,0,0,3,1,3,3,0],
[0,3,3,1,7,4,4,4,4,4,8,1,7,4,4,4,4,8,1,7,4,4,4,4,4,8,1,3,3,0],
[0,3,3,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,3,3,0],
[0,3,7,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,8,3,0],
[0,7,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,8,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]

level = copy.deepcopy(boards)
# Loads present image
present_image = pygame.transform.scale(pygame.image.load('map_assets/present.png'), (15,15))
# Loads candy image
candy_image = pygame.transform.scale(pygame.image.load('map_assets/candy.png'), (25,25))

def draw_level_elements(level):
    # Map each tile type to its respective drawing function
    shapes = {
        PRESENT: lambda i, j: screen.blit(present_image, (j * column_spacing + (0.3 * column_spacing), i * row_spacing + (0.3 * row_spacing))),
        CANDY: lambda i, j: screen.blit(candy_image, (j * column_spacing + (0.3 * column_spacing), i * row_spacing + (0.3 * row_spacing))),
        VERTICAL_LINE: lambda i, j: pygame.draw.line(screen, 'red', (j * column_spacing + (0.5 * column_spacing), i * row_spacing), (j * column_spacing + (0.5 * column_spacing), i * row_spacing + row_spacing), 3),
        HORIZONTAL_LINE: lambda i, j: pygame.draw.line(screen, 'red', (j * column_spacing, i * row_spacing + (0.5 * row_spacing)), (j * column_spacing + column_spacing, i * row_spacing + (0.5 * row_spacing)), 3),
        TOP_RIGHT: lambda i, j: pygame.draw.arc(screen, 'red', [(j * column_spacing - (column_spacing * 0.4)) - 2, (i * row_spacing + (0.5 * row_spacing)), column_spacing, row_spacing], 0, PI / 2, 3),
        TOP_LEFT: lambda i, j: pygame.draw.arc(screen, 'red', [(j * column_spacing + (column_spacing * 0.5)), (i * row_spacing + (0.5 * row_spacing)), column_spacing, row_spacing], PI / 2, PI, 3),
        BOTTOM_LEFT: lambda i, j: pygame.draw.arc(screen, 'red', [(j * column_spacing + (column_spacing * 0.5)), (i * row_spacing - (0.4 * row_spacing)), column_spacing, row_spacing], PI, 3 * PI / 2, 3),
        BOTTOM_RIGHT: lambda i, j: pygame.draw.arc(screen, 'red', [(j * column_spacing - (column_spacing * 0.4)) - 2, (i * row_spacing - (0.4 * row_spacing)), column_spacing, row_spacing], 3 * PI / 2, 2 * PI, 3),
    }

    # Iterate through the level and draw the corresponding shapes
    for i, row in enumerate(level):
        for j, tile in enumerate(row):
            # Check if the tile type has a corresponding drawing function
            if tile in shapes:
                # Execute the drawing function for the specific tile
                shapes[tile](i, j)
    
