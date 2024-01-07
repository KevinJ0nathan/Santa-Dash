import pygame
from constants import *
from level import level
from level import EMPTY, PRESENT, CANDY

class Player():
    def __init__(self):

        # Initialize the starting position
        self.position_x = START_PLAYER_X
        self.position_y = START_PLAYER_Y
        # Initialize the direction in which the player is moving
        self.direction = RIGHT
        # Initialize the player's speed
        self.speed = 2
        # Initialize which turns are allowed (R L U D)
        self.turns_allowed = [False,False,False,False]

    def draw(self, direction, position_x, position_y, counter):
        # Depending on the 'direction' variable, different transformations of the player image are performed and drawn on the screen

        # If the direction is RIGHT, draw the player image at the given position
        if direction == RIGHT:
            screen.blit(player_images[counter // 5], (position_x, position_y))
        
        # If the direction is LEFT, flip the player image horizontally and draw it at the given position
        elif direction == LEFT:
            flipped_image = pygame.transform.flip(player_images[counter // 5], True, False)
            screen.blit(flipped_image, (position_x, position_y))
        
        # If the direction is UP, rotate the player image 90 degrees clockwise and draw it at the given position
        elif direction == UP:
            rotated_image = pygame.transform.rotate(player_images[counter // 5], 90)
            screen.blit(rotated_image, (position_x, position_y))
        
        # If the direction is DOWN, rotate the player image 270 degrees clockwise (or 90 degrees counter-clockwise) and draw it at the given position
        elif direction == DOWN:
            rotated_image = pygame.transform.rotate(player_images[counter // 5], 270)
            screen.blit(rotated_image, (position_x, position_y))

    def check_position(self, player_center_x, player_center_y, direction):
         # Initialize a list to track possible turns in each direction
        turns = [False, False, False, False]
        # Calculate the index of the player's current column and row
        column_index = player_center_x // column_spacing
        row_index = player_center_y // row_spacing

        # Check for possible movements based on direction and wall collision detection
        if player_center_x // 30 < 29:
            if direction == RIGHT:
                # Check for collision when moving right
                if level[row_index][(player_center_x - fudge_factor) // column_spacing] < 3:
                    turns[LEFT] = True
            elif direction == LEFT:
                 # Check for collision when moving left
                if level[row_index][(player_center_x + fudge_factor) // column_spacing] < 3:
                    turns[RIGHT] = True
            elif direction == UP:
                # Check for collision when moving up
                if level[(player_center_y + fudge_factor) // row_spacing][column_index] < 3:
                    turns[DOWN] = True
            elif direction == DOWN:
                # Check for collision when moving down
                if level[(player_center_y - fudge_factor) // row_spacing][column_index] < 3:
                    turns[UP] = True

            
            if direction in (UP, DOWN):
                # Making sure the player is roughly in the middle of the grid or tile
                if 12 <= player_center_x % column_spacing <= 18:
                    # Additional collision checks for UP and DOWN movements
                    if level[(player_center_y + fudge_factor) // row_spacing][column_index] < 3:
                        turns[DOWN] = True
                    if level[(player_center_y - fudge_factor) // row_spacing][column_index] < 3:
                        turns[UP] = True
                if 12 <= player_center_y % row_spacing <= 18:
                    if level[row_index][(player_center_x - column_spacing) // column_spacing] < 3:
                        turns[LEFT] = True
                    if level[row_index][(player_center_x + column_spacing) // column_spacing] < 3:
                        turns[RIGHT] = True

            if direction in (RIGHT, LEFT):
                  # Making sure the player is roughly in the middle of the grid or tile
                if 12 <= player_center_x % column_spacing <= 18:
                     # Additional collision checks for RIGHT and LEFT movements
                    if level[(player_center_y + row_spacing) // row_spacing][column_index] < 3:
                        turns[DOWN] = True
                    if level[(player_center_y - row_spacing) // row_spacing][column_index] < 3:
                        turns[UP] = True
                if 12 <= player_center_y % row_spacing <= 18:
                    if level[row_index][(player_center_x - fudge_factor) // column_spacing] < 3:
                        turns[LEFT] = True
                    if level[row_index][(player_center_x + fudge_factor) // column_spacing] < 3:
                        turns[RIGHT] = True
        else:
            turns[RIGHT] = True
            turns[LEFT] = True

        return turns

    def move_player(self, player_position_x, player_position_y, direction, turns_allowed, speed):
            # Move the player according to the allowed directions and speed
            if direction == RIGHT and turns_allowed[RIGHT]:
                player_position_x += speed
            elif direction == LEFT and turns_allowed[LEFT]:
                player_position_x -= speed
            if direction == UP and turns_allowed[UP]:
                player_position_y -= speed
            elif direction == DOWN and turns_allowed[DOWN]:
                player_position_y += speed
            # Return the updated player position
            return player_position_x, player_position_y
    

    def check_collisions(self, score, player_center_x, player_center_y, powerUp, power_counter, level):
        # Define spacing based on screen dimensions
        row_spacing = (screen_height - 50) // 32
        column_spacing = screen_width // 30
        
        # Check if the player is within the horizontal bounds of the game area
        if 0 < player_center_x < 870:
            # Check if the player's current position corresponds to a present item
            if level[player_center_y // row_spacing][player_center_x // column_spacing] == PRESENT:
                # If a present is found at the player's position, remove it and increase the score by 10
                level[player_center_y // row_spacing][player_center_x // column_spacing] = 0
                score += 10
                score_sound.play()

            # Check if the player's current position corresponds to a big dot item
            if level[player_center_y // row_spacing][player_center_x // column_spacing] == CANDY:
                # If a big dot is found at the player's position, remove it and increase the score by 50
                level[player_center_y // row_spacing][player_center_x // column_spacing] = 0
                score += 50
                score_sound.play()
                # For Powerup
                powerUp = True
                power_counter = 0
        
        # Return the updated score after checking collisions
        return score, powerUp, power_counter
