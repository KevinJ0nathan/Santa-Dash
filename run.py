import pygame
from constants import *
from level import *
from player import Player
from scoreboard import *
from enemy import Enemy

# Initialize Pygame mixer
pygame.mixer.init()

# Load the song
pygame.mixer.music.load('game_sounds/game_bgm.wav') 

# Play the song in an infinite loop (-1 means infinite loop)
pygame.mixer.music.play(-1)

# Set the initial volume to 0.5 (half of the maximum volume)
pygame.mixer.music.set_volume(0.5)
# Set the window icon
pygame.display.set_icon(icon_image)
# Sets the caption of the window
pygame.display.set_caption('Santa Dash')
# Initializes the player object
player = Player()

# If game is running
running = True
# Main game loop
while running:
    # sets the fps
    timer.tick(fps)

    # Main loop for image animation
    if counter < MAX_COUNTER:
        counter += 1
    else:
        # Reset counter
        counter = 0


    # Check if power-up is active and within duration
    if powerUp and power_counter < MAX_POWER_DURATION:
        # Increment the power-up timer
        power_counter += 1
    # If power-up duration is reached
    elif powerUp and power_counter >= MAX_POWER_DURATION:
        # Reset the power-up timer
        power_counter = 0
        # Deactivate the power-up
        powerUp = False

     # Check if debuff is active and within duration
    if debuff and debuff_timer < MAX_DEBUFF_DURATION:
         # Increment the debuff timer
         debuff_timer += 1
         # If debuff duration is reached
    elif debuff and debuff_timer >= MAX_DEBUFF_DURATION:
         # Reset the debuff timer
         debuff_timer = 0
         # Deactivate the debuff
         debuff = False

    # Startup counter
    if startup_counter < STARTUP_DURATION and not game_over and not game_won:
        # Disables movement
        moving = False
        # Increment the start up timer
        startup_counter += 1
    elif game_over or game_won:
         # Disables movement of player and enemy when game is over or game is won
         moving = False
    else:
        # Allows movement
        moving = True

    # sets the background
    screen.fill(('white'))
    # Draws the level elements into the screen
    draw_level_elements(level)
    # Updates the player's center position
    player_center_x = player.position_x + OFFSET_X
    player_center_y = player.position_y + OFFSET_Y
    player_circle = pygame.draw.circle(screen, 'white', (player_center_x, player_center_y), 10, 2)
    # Draw the player on the screen based on its current direction and position
    player.draw(player.direction, player.position_x, player.position_y, counter)
    # Check allowed turns for the player based on its current position and direction
    turns_allowed = player.check_position(player_center_x, player_center_y, player.direction)

    # Check collisions for the player's new position and update the score and powerUp accordingly
    score, powerUp, power_counter = player.check_collisions(score, player_center_x, player_center_y, powerUp, power_counter, level)
  
    # Sets the target position for the enemies as the player's position
    targets = [(player.position_x, player.position_y)]

    # Evil Snowman Object
    evilSnowman = Enemy(evilSnowman_position_x, evilSnowman_position_y, modified_evilSnowman_speed, evilSnowman_direction , targets[0], evilSnowman_images)
    evilSnowman.draw()
    
    # Ice spirit Object
    iceSpirit = Enemy(iceSpirit_position_x, iceSpirit_position_y, modified_iceSpirit_speed, iceSpirit_direction , targets[0], iceSpirit_images)
    iceSpirit.draw()

    # Thief Object
    Thief =  Enemy(thief_position_x, thief_position_y, modified_thief_speed, thief_direction , targets[0], thief_images)
    Thief.draw()

    # Display the score, highscore, lives and game over or game won 
    draw_misc(score, lives, game_over, game_won, highscore)

    # Keep the original player's speed in a variable
    original_player_speed = player.speed

    # Checker the current score is greater than the high score, then set it as the highscore
    if score > highscore:
         highscore = score

    if powerUp:
        # Half the enemies' speed
        modified_iceSpirit_speed = iceSpirit_speed // 2
        modified_evilSnowman_speed = evilSnowman_speed // 2
        modified_thief_speed = thief_speed // 2
    else:
        # Set the enemies' speed back to the original value
        modified_iceSpirit_speed = iceSpirit_speed
        modified_evilSnowman_speed = evilSnowman_speed
        modified_thief_speed = thief_speed
   
    if debuff:
         # Apply speed modification if debuff is active
         modified_speed = original_player_speed // 2
    else:
         # Returns player's speed to the original speed
         modified_speed = original_player_speed


    if moving:
        # Update positions based on movement and modified speed
        player.position_x, player.position_y = player.move_player(player.position_x, player.position_y, player.direction, turns_allowed, modified_speed)
        evilSnowman_position_x, evilSnowman_position_y, evilSnowman_direction = evilSnowman.move_enemy()
        iceSpirit_position_x, iceSpirit_position_y, iceSpirit_direction = iceSpirit.move_IceSpirit()
        thief_position_x, thief_position_y, thief_direction = Thief.move_Thief()
    # Santa dies if collides with snowman
    if player_circle.colliderect(evilSnowman.rect):
        if lives > 0:
            lives -= LIVES_PENALTY
            startup_counter = 0
            # Reset positions and directions
            player.position_x = START_PLAYER_X
            player.position_y = START_PLAYER_Y
            player.direction = RIGHT
            direction_command = RIGHT
            evilSnowman_position_x = START_EVIL_SNOWMAN_X
            evilSnowman_position_y = START_EVIL_SNOWMAN_Y
            evilSnowman_direction = RIGHT
            iceSpirit_position_x = START_ICE_SPIRIT_X
            iceSpirit_position_y = START_ICE_SPIRIT_Y
            iceSpirit_direction = RIGHT
            thief_position_x = START_THIEF_X
            thief_position_y = START_THIEF_Y
            thief_direction = RIGHT
            powerUp = False
            debuff = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    # If player collides with ice spirit, activate debuff for the player and start the timer
    elif player_circle.colliderect(iceSpirit.rect):
         if powerUp ==  False:
              debuff = True
              debuff_timer = 0
    # If player collides with thief, reduce score
    elif player_circle.colliderect(Thief.rect):
        if score > 0:
         score -= SCORE_PENALTY


   
    for event in pygame.event.get():
         # To exit out of the game
        if event.type == pygame.QUIT:
            running = False
        
        # Check for arrow inputs for santa movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = RIGHT
            if event.key == pygame.K_LEFT:
                direction_command = LEFT
            if event.key == pygame.K_UP:
                direction_command = UP
            if event.key == pygame.K_DOWN:
                direction_command = DOWN
            if event.key == pygame.K_SPACE and (game_over or game_won):
                # Resets everything back to the original values
                startup_counter = 0
                # Reset positions and directions
                player.position_x = START_PLAYER_X
                player.position_y = START_PLAYER_Y
                player.direction = RIGHT
                direction_command = RIGHT
                evilSnowman_position_x = START_EVIL_SNOWMAN_X
                evilSnowman_position_y = START_EVIL_SNOWMAN_Y
                evilSnowman_direction = RIGHT
                iceSpirit_position_x = START_ICE_SPIRIT_X
                iceSpirit_position_y = START_ICE_SPIRIT_Y
                iceSpirit_direction = RIGHT
                thief_position_x = START_THIEF_X
                thief_position_y = START_THIEF_Y
                thief_direction = RIGHT
                powerUp = False
                debuff = False
                score = 0
                lives = 3
                level = copy.deepcopy(boards)
                game_won = False
                game_over = False
        
        # Sets the player direction if its allowed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == RIGHT:
                direction_command = player.direction
            if event.key == pygame.K_LEFT and direction_command == LEFT:
                direction_command = player.direction
            if event.key == pygame.K_UP and direction_command == UP:
                direction_command = player.direction
            if event.key == pygame.K_DOWN and direction_command == DOWN:
                direction_command = player.direction

    # Changes direction of player if its allowed
    if direction_command == RIGHT and turns_allowed[RIGHT]:
            player.direction = RIGHT
    if direction_command == LEFT and turns_allowed[LEFT]:
            player.direction = LEFT
    if direction_command == UP and turns_allowed[UP]:
            player.direction = UP
    if direction_command == DOWN and turns_allowed[DOWN]:
            player.direction = DOWN

    # Check if player_center_x is beyond the right boundary
    if player_center_x > RIGHT_BOUNDARY:
        # Reset player_center_x and update player position for continuous movement
        player_center_x = RESET_RIGHT
        player.position_x = player_center_x + MOVEMENT_OFFSET

    # Check if player_center_x is beyond the left boundary
    elif player_center_x < LEFT_BOUNDARY:
        # Reset player_center_x and update player position for continuous movement
        player_center_x = RESET_LEFT
        player.position_x = player_center_x - MOVEMENT_OFFSET
    
    game_won = True
    # For loop to check if there are still presents and candy in the map
    for i in range(len(level)):
         if PRESENT in level[i] or CANDY in level[i]:
              game_won = False

    # Drawing/rendering goes here
    pygame.display.flip()

# When the loop exits (user closes window or program), stop the music and quit Pygame
pygame.mixer.music.stop()
pygame.quit()  # Close Pygame when the loop ends
