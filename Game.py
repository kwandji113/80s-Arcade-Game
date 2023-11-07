import pygame
import playerState
from screenState import screenState
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Street Fighter with a Twist ")

players = {}
game_screen = screenState(screen)

# Screen flags

background_image1 = pygame.image.load("testimage.jpg")
background_image1 = pygame.transform.scale(background_image1, (SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font(None, 36)


# Button data for Screen 2
buttons_screen2 = ["Green", "Yellow", "Blue", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

# Main loop
running = True
char_selected = 0
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_screen.current_screen != 3 or game_screen.current_screen != 1:
                    game_screen.current_screen += 1
            elif game_screen.current_screen == 1:
                if event.key == pygame.K_RETURN:
                    # Add code to perform actions when a button is selected
                    print(f"Button '{buttons_screen2[game_screen.button_pos[0] + game_screen.button_pos[1]*4]}' selected.")

    if game_screen.current_screen == 0:
        game_screen.start_screen()
    elif game_screen.current_screen == 1:
        game_screen.champ_select_screen(events, players)

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()