import pygame 
from constants import *
from level import level



class Enemy():
    # Initialize enemy attributes
    def __init__(self, position_x, position_y, speed, direction, targets, img):
        # X-coordinate of enemy
        self.position_x = position_x
        # Y-coordinate of enemy
        self.position_y = position_y
        # Center X-coordinate of enemy
        self.center_x = self.position_x + OFFSET_ENEMY
        # Center Y-coordinate of enemy
        self.center_y = self.position_y + OFFSET_ENEMY
        # Images representing the enemy
        self.enemy_images = img
        # Speed of the enemy
        self.speed = speed
        # Current direction of the enemy
        self.direction = direction
        # Check for available turns around the enemy
        self.turns = self.check_collisions()
        # Set the target coordinates for the enemy
        self.targets = targets
        # Create a rectangular collision object around the enemy
        self.rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))

    # Draws the enemy and rotates them based on the direction they are going
    def draw(self):
        if self.direction == RIGHT:
            # If the direction is RIGHT, blit the enemy image at its current position
            screen.blit(self.enemy_images, (self.position_x, self.position_y))
        elif self.direction == LEFT:
            # If the direction is LEFT, flip the enemy image horizontally and blit it
            screen.blit(pygame.transform.flip(self.enemy_images, True, False), (self.position_x, self.position_y))
        elif self.direction == UP:
            # If the direction is UP, rotate the enemy image 90 degrees clockwise and blit it
            screen.blit(pygame.transform.rotate(self.enemy_images, 90), (self.position_x, self.position_y))
        elif self.direction == DOWN:
             # If the direction is DOWN, rotate the enemy image 270 degrees clockwise (or 90 degrees counterclockwise) and blit it
            screen.blit(pygame.transform.rotate(self.enemy_images, 270), (self.position_x, self.position_y))

    def check_collisions(self):
        # Right, Left, Up, Down
        # Initialize a list to track if there are possible turns in each direction
        self.turns = [False, False, False, False]
        
        # Function to check collision in a specific direction
        def check_direction(dy, dx, index):
            # Calculate the coordinates of the adjacent tile
            new_y = (self.center_y + dy) // row_spacing
            new_x = (self.center_x + dx) // column_spacing
            
            # Check if the calculated coordinates are within the level boundaries
            if 0 <= new_y < len(level) and 0 <= new_x < len(level[0]):
                # Get the value of the tile in the level map
                tile_value = level[new_y][new_x]
                # Check if the tile allows movement
                if tile_value in [EMPTY, PRESENT, CANDY]:
                    # Update the corresponding index in turns list if movement is allowed
                    self.turns[index] = True
        
        # Check adjacent tiles in all directions
        # Check rightward tile
        check_direction(0, column_spacing, RIGHT)
        # Check leftward tile
        check_direction(0, -column_spacing, LEFT)
        # Check upward tile
        check_direction(-row_spacing, 0, UP)
        # Check downward tile
        check_direction(row_spacing, 0, DOWN)
        
        # Return the list indicating the availability of turns in different directions
        return self.turns


    def move_enemy(self):
            #r l u d
            # enemy is going to turn whenever advantageous for pursuit
            # When the snowman is moving right
            if self.direction == RIGHT:
                # If the target's x position is greater than the enemy's current x position and the enemy is able to turn right, then turn right
                if self.targets[x_pos] > self.position_x and self.turns[RIGHT]:
                    self.position_x += self.speed
                # If the enemy is not able to turn right
                elif not self.turns[RIGHT]:
                    # If the target's y position is below the enemy's current y position and the enemy is able to turn down, then turn down
                    if self.targets[y_pos] > self.position_y and self.turns[DOWN]:
                        self.direction = DOWN
                        self.position_y += self.speed
                    # If the target's y position is above the enemy's current y position and the enemy is able to turn up, then turn up
                    elif self.targets[y_pos] < self.position_y and self.turns[UP]:
                        self.direction = UP
                        self.position_y -= self.speed
                    # If the target's x position is to the left of the enemy's current x position and the enemy is able to turn left, then turn left
                    elif self.targets[x_pos] < self.position_x and self.turns[LEFT]:
                        self.direction = LEFT
                        self.position_x -= self.speed
                    # If none of the above conditions were accepted
                    # If enemy is able to turn down, then turn down
                    elif self.turns[DOWN]:
                        self.direction = DOWN
                        self.position_y += self.speed
                    # If enemy is able to turn UP, then turn UP
                    elif self.turns[UP]:
                        self.direction = UP
                        self.position_y -= self.speed
                    # If enemy is able to turn left, then turn left
                    elif self.turns[LEFT]:
                        self.direction = LEFT
                        self.position_x -= self.speed
                # If the enemy can turn or is moving right, but the target is not on the right
                elif self.turns[RIGHT]:
                    # If the target is below the enemy, turn down
                    if self.targets[y_pos] > self.position_y and self.turns[DOWN]:
                        self.direction = DOWN
                        self.position_y += self.speed
                    # If the target is above the enemy, turn up
                    if self.targets[y_pos] < self.position_y and self.turns[UP]:
                        self.direction = UP
                        self.position_y -= self.speed
                    else:
                        self.position_x += self.speed
            # Check for other directions if unable to turn left or target not on the left
            elif self.direction == LEFT:
                if self.targets[y_pos] > self.position_y and self.turns[DOWN]:
                    self.direction = DOWN
                    self.position_y += self.speed
                elif self.targets[x_pos] < self.position_x and self.turns[LEFT]:
                    self.position_x -= self.speed
                elif not self.turns[LEFT]:
                    if self.targets[y_pos] > self.position_y and self.turns[DOWN]:
                        self.direction = DOWN
                        self.position_y += self.speed
                    elif self.targets[y_pos] < self.position_y and self.turns[UP]:
                        self.direction = UP
                        self.position_y -= self.speed
                    elif self.targets[x_pos] > self.position_x and self.turns[RIGHT]:
                        self.direction = RIGHT
                        self.position_x += self.speed
                    # Move in available directions if unable to turn towards the target
                    elif self.turns[DOWN]:
                        self.direction = DOWN
                        self.position_y += self.speed
                    elif self.turns[UP]:
                        self.direction = UP
                        self.position_y -= self.speed
                    elif self.turns[RIGHT]:
                        self.direction = RIGHT
                        self.position_x += self.speed
                elif self.turns[LEFT]:
                    if self.targets[y_pos] > self.position_y and self.turns[DOWN]:
                        self.direction = DOWN
                        self.position_y += self.speed
                    if self.targets[y_pos] < self.position_y and self.turns[UP]:
                        self.direction = UP
                        self.position_y -= self.speed
                    else:
                        self.position_x -= self.speed

            elif self.direction == UP:
                if self.targets[x_pos] < self.position_x and self.turns[LEFT]:
                    self.direction = LEFT
                    self.position_x -= self.speed
                elif self.targets[y_pos] < self.position_y and self.turns[UP]:
                    self.direction = UP
                    self.position_y -= self.speed
                elif not self.turns[UP]:
                    if self.targets[x_pos] > self.position_x and self.turns[RIGHT]:
                        self.direction = RIGHT
                        self.position_x += self.speed
                    elif self.targets[x_pos] < self.position_x and self.turns[LEFT]:
                        self.direction = LEFT
                        self.position_x -= self.speed
                    elif self.targets[y_pos] > self.position_y and self.turns[DOWN]:
                        self.direction = DOWN
                        self.position_y += self.speed
                    elif self.turns[LEFT]:
                        self.direction = LEFT
                        self.position_x -= self.speed
                    elif self.turns[DOWN]:
                        self.direction = DOWN
                        self.position_y += self.speed
                    elif self.turns[RIGHT]:
                        self.direction = RIGHT
                        self.position_x += self.speed
                elif self.turns[UP]:
                    if self.targets[x_pos] > self.position_x and self.turns[RIGHT]:
                        self.direction = RIGHT
                        self.position_x += self.speed
                    elif self.targets[x_pos] < self.position_x and self.turns[LEFT]:
                        self.direction = LEFT
                        self.position_x -= self.speed
                    else:
                        self.position_y -= self.speed

            elif self.direction == DOWN:
                if self.targets[y_pos] > self.position_y and self.turns[DOWN]:
                    self.position_y += self.speed
                elif not self.turns[DOWN]:
                    if self.targets[x_pos] > self.position_x and self.turns[RIGHT]:
                        self.direction = RIGHT
                        self.position_x += self.speed
                    elif self.targets[x_pos] < self.position_x and self.turns[LEFT]:
                        self.direction = LEFT
                        self.position_x -= self.speed
                    elif self.targets[y_pos] < self.position_y and self.turns[UP]:
                        self.direction = UP
                        self.position_y -= self.speed
                    elif self.turns[LEFT]:
                        self.direction = LEFT
                        self.position_x -= self.speed
                    elif self.turns[UP]:
                        self.direction = UP
                        self.position_y -= self.speed
                    elif self.turns[RIGHT]:
                        self.direction = RIGHT
                        self.position_x += self.speed
                elif self.turns[DOWN]:
                    if self.targets[x_pos] > self.position_x and self.turns[RIGHT]:
                        self.direction = RIGHT
                        self.position_x += self.speed
                    elif self.targets[x_pos] < self.position_x and self.turns[LEFT]:
                        self.direction = LEFT
                        self.position_x -= self.speed
                    else:
                        self.position_y += self.speed

            # Makes the snowman seamlessly move to left or right
            if self.position_x < LEFT_BOUNDARY:
                self.position_x = RESET_LEFT - MOVEMENT_OFFSET
            elif self.position_x > RIGHT_BOUNDARY:
                self.position_x = RESET_RIGHT + MOVEMENT_OFFSET

            return self.position_x, self.position_y, self.direction
    

    def move_IceSpirit(self):
        # r, l, u, d
        # Icespirit is going to turn whenever colliding with walls, otherwise continue straight
        if self.direction == RIGHT:
            if self.targets[x_pos] > self.position_x and self.turns[RIGHT]:
                self.position_x += self.speed
            elif not self.turns[RIGHT]:
                if self.targets[y_pos] > self.position_y and self.turns[DOWN]:
                    self.direction = DOWN
                    self.position_y += self.speed
                elif self.targets[y_pos] < self.position_y and self.turns[UP]:
                    self.direction = UP
                    self.position_y -= self.speed
                elif self.targets[x_pos] < self.position_x and self.turns[LEFT]:
                    self.direction = LEFT
                    self.position_x -= self.speed
                elif self.turns[DOWN]:
                    self.direction = DOWN
                    self.position_y += self.speed
                elif self.turns[UP]:
                    self.direction = UP
                    self.position_y -= self.speed
                elif self.turns[DOWN]:
                    self.direction = 1
                    self.position_x -= self.speed
            elif self.turns[RIGHT]:
                self.position_x += self.speed
        elif self.direction == LEFT:
            if self.targets[x_pos] < self.position_x and self.turns[LEFT]:
                self.position_x -= self.speed
            elif not self.turns[LEFT]:
                if self.targets[y_pos] > self.position_y and self.turns[DOWN]:
                    self.direction = DOWN
                    self.position_y += self.speed
                elif self.targets[y_pos] < self.position_y and self.turns[UP]:
                    self.direction = UP
                    self.position_y -= self.speed
                elif self.targets[x_pos] > self.position_x and self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.position_x += self.speed
                elif self.turns[DOWN]:
                    self.direction = DOWN
                    self.position_y += self.speed
                elif self.turns[UP]:
                    self.direction = UP
                    self.position_y -= self.speed
                elif self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.position_x += self.speed
            elif self.turns[LEFT]:
                self.position_x -= self.speed
        elif self.direction == UP:
            if self.targets[y_pos] < self.position_y and self.turns[UP]:
                self.direction = UP
                self.position_y -= self.speed
            elif not self.turns[UP]:
                if self.targets[x_pos] > self.position_x and self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.position_x += self.speed
                elif self.targets[x_pos] < self.position_x and self.turns[LEFT]:
                    self.direction = LEFT
                    self.position_x -= self.speed
                elif self.targets[y_pos] > self.position_y and self.turns[DOWN]:
                    self.direction = DOWN
                    self.position_y += self.speed
                elif self.turns[DOWN]:
                    self.direction = DOWN
                    self.position_y += self.speed
                elif self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.position_x += self.speed
                elif self.turns[LEFT]:
                    self.direction = LEFT
                    self.position_x -= self.speed
            elif self.turns[UP]:
                self.position_y -= self.speed
        elif self.direction == DOWN:
            if self.targets[y_pos] > self.position_y and self.turns[DOWN]:
                self.position_y += self.speed
            elif not self.turns[DOWN]:
                if self.targets[x_pos] > self.position_x and self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.position_x += self.speed
                elif self.targets[x_pos] < self.position_x and self.turns[LEFT]:
                    self.direction = LEFT
                    self.position_x -= self.speed
                elif self.targets[y_pos] < self.position_y and self.turns[UP]:
                    self.direction = UP
                    self.position_y -= self.speed
                elif self.turns[UP]:
                    self.direction = UP
                    self.position_y -= self.speed
                elif self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.position_x += self.speed
                elif self.turns[LEFT]:
                    self.direction = LEFT
                    self.position_x -= self.speed
            elif self.turns[DOWN]:
                self.position_y += self.speed
        if self.position_x < LEFT_BOUNDARY:
                self.position_x = RESET_LEFT - MOVEMENT_OFFSET
        elif self.position_x > RIGHT_BOUNDARY:
                self.position_x = RESET_RIGHT + MOVEMENT_OFFSET
        return self.position_x, self.position_y, self.direction

    def move_Thief(self):
        # turns up or down at any point to pursue, but left and right only on collision
        if self.direction == RIGHT:
            if self.targets[x_pos] > self.position_x and self.turns[RIGHT]:
                self.position_x += self.speed
            elif not self.turns[RIGHT]:
                if self.targets[y_pos] > self.position_y and self.turns[DOWN]:
                    self.direction = DOWN
                    self.position_y += self.speed
                elif self.targets[y_pos] < self.position_y and self.turns[UP]:
                    self.direction = UP
                    self.position_y -= self.speed
                elif self.targets[x_pos] < self.position_x and self.turns[LEFT]:
                    self.direction = LEFT
                    self.position_x -= self.speed
                elif self.turns[DOWN]:
                    self.direction = DOWN
                    self.position_y += self.speed
                elif self.turns[UP]:
                    self.direction = UP
                    self.position_y -= self.speed
                elif self.turns[LEFT]:
                    self.direction = LEFT
                    self.position_x -= self.speed
            elif self.turns[RIGHT]:
                if self.targets[y_pos] > self.position_y and self.turns[DOWN]:
                    self.direction = DOWN
                    self.position_y += self.speed
                if self.targets[y_pos] < self.position_y and self.turns[UP]:
                    self.direction = UP
                    self.position_y -= self.speed
                else:
                    self.position_x += self.speed
        elif self.direction == LEFT:
                if self.targets[y_pos] > self.position_y and self.turns[DOWN]:
                    self.direction = DOWN
                elif self.targets[x_pos] < self.position_x and self.turns[LEFT]:
                    self.position_x -= self.speed
                elif not self.turns[LEFT]:
                    if self.targets[y_pos] > self.position_y and self.turns[DOWN]:
                        self.direction = DOWN
                        self.y_pos += self.speed
                    elif self.targets[y_pos] < self.position_y and self.turns[UP]:
                        self.direction = UP
                        self.position_y -= self.speed
                    elif self.targets[x_pos] > self.position_x and self.turns[RIGHT]:
                        self.direction = RIGHT
                        self.position_x += self.speed
                    elif self.turns[DOWN]:
                        self.direction = DOWN
                        self.position_y += self.speed
                    elif self.turns[UP]:
                        self.direction = UP
                        self.position_y -= self.speed
                    elif self.turns[RIGHT]:
                        self.direction = RIGHT
                        self.position_x += self.speed
                elif self.turns[LEFT]:
                    if self.targets[y_pos] > self.position_y and self.turns[DOWN]:
                        self.direction = DOWN
                        self.position_y += self.speed
                    if self.targets[y_pos] < self.position_y and self.turns[UP]:
                        self.direction = UP
                        self.position_y -= self.speed
                    else:
                        self.position_x -= self.speed
        elif self.direction == UP:
                if self.targets[y_pos] < self.position_y and self.turns[UP]:
                    self.direction = UP
                    self.position_y -= self.speed
                elif not self.turns[UP]:
                    if self.targets[x_pos] > self.position_x and self.turns[RIGHT]:
                        self.direction = RIGHT
                        self.position_x += self.speed
                    elif self.targets[x_pos] < self.position_x and self.turns[LEFT]:
                        self.direction = LEFT
                        self.position_x -= self.speed
                    elif self.targets[y_pos] > self.position_y and self.turns[UP]:
                        self.direction = UP
                        self.position_y += self.speed
                    elif self.turns[LEFT]:
                        self.direction = LEFT
                        self.position_x -= self.speed
                    elif self.turns[DOWN]:
                        self.direction = DOWN
                        self.position_y += self.speed
                    elif self.turns[RIGHT]:
                        self.direction = RIGHT
                        self.position_x += self.speed
                elif self.turns[UP]:
                    self.position_y -= self.speed
        elif self.direction == DOWN:
                if self.targets[y_pos] > self.position_y and self.turns[DOWN]:
                    self.position_y += self.speed
                elif not self.turns[DOWN]:
                    if self.targets[x_pos] > self.position_x and self.turns[RIGHT]:
                        self.direction = RIGHT
                        self.position_x += self.speed
                    elif self.targets[x_pos] < self.position_x and self.turns[LEFT]:
                        self.direction = LEFT
                        self.position_x -= self.speed
                    elif self.targets[y_pos] < self.position_y and self.turns[UP]:
                        self.direction = UP
                        self.position_y -= self.speed
                    elif self.turns[UP]:
                        self.direction = UP
                        self.position_y -= self.speed
                    elif self.turns[LEFT]:
                        self.direction = LEFT
                        self.position_xs -= self.speed
                    elif self.turns[RIGHT]:
                        self.direction = RIGHT
                        self.position_x += self.speed
                elif self.turns[DOWN]:
                    self.position_y += self.speed

        if self.position_x < LEFT_BOUNDARY:
                self.position_x = RESET_LEFT - MOVEMENT_OFFSET
        elif self.position_x > RIGHT_BOUNDARY:
                self.position_x = RESET_RIGHT + MOVEMENT_OFFSET

        return self.position_x, self.position_y, self.direction
