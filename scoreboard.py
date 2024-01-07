import pygame
from constants import *

# Function to draw various game elements on the screen
def draw_misc(score, lives, game_over, game_won, highscore):
    # Rendering text for score and highscore
    score_text = font.render(f'Score: {score}', True, 'black')
    highscore_text = font.render(f'Highscore: {highscore}', True, 'black')
    # Displaying score and highscore on the screen
    screen.blit(score_text, score_position)
    screen.blit(highscore_text, highscore_position)
    # Displaying player lives as small images on the screen
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0],PLAYER_LIVES_SIZE), (PLAYER_LIVES_START_POS_X + i * PLAYER_LIVES_GAP, PLAYER_LIVES_START_POS_Y))
    # Displaying game over screen if the game is over
    if game_over:
        screen.blit(game_over_image,(0,0))
    # Displaying victory screen if the game is won
    if game_won:
        screen.blit(victory_image, (0, 0))  