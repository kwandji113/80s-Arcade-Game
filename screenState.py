import pygame
import os
from playerState import playerState

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

class screenState():
    
    def __init__(self, game_screen) -> None:
        self.game_screen = game_screen
        self.font = pygame.font.Font(None, 36)
        self.start_screen_background = pygame.image.load(os.path.join('Backgrounds', "testimage.jpg"))
        self.start_screen_background = pygame.transform.scale(self.start_screen_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.select_screen_background = pygame.image.load(os.path.join('Backgrounds', "Character Select Background.jpg"))
        self.select_screen_background = pygame.transform.scale(self.select_screen_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.current_screen = 0
        self.map_selected = None
        self.screens = []
        self.button_pos = [0, 0]
        self.char_selected = 0
        self.char_buttons = ["Green", "Yellow", "Blue", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
        self.map_testing = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]
        self.map_backgrounds = ["Blanka Stage.png", "E Honda Stage (1).png", "Guile Stage.png", "Ken Stage.png", "Ryu Stage (1).png", "Zangief Stage (1).png"]
        self.map_buttons = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
        self.current_map = 2


    def update_screen(self, events, players):
        if self.current_screen == 0:
            self.start_screen()
        elif self.current_screen == 1:
            self.champ_select_screen(events, players)
        elif self.current_screen == 2:
            # self.map_select_screen(events)
            self.map_carousel_select_screen(events)
        elif self.current_screen == 3:
            self.fight_screen()

    def start_screen(self):
        start_text = self.font.render("PRESS SPACE TO START", 1, (0, 0, 0))
        start_text_pos = start_text.get_rect()
        start_text_pos.center = self.start_screen_background.get_rect().center
        start_text_pos.y += 200
        self.game_screen.blit(self.start_screen_background, self.start_screen_background.get_rect())
        self.game_screen.blit(start_text, start_text_pos)

    def champ_select_screen(self, events, players):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.select_controls(event.key):
                    players[f"{self.char_selected}"] = self.char_buttons[self.button_pos[0] + self.button_pos[1]*4]
                    self.char_selected += 1
                    if self.char_selected == 2:
                        self.current_screen += 1
        self.draw_select_boxes(True)
        return players

    def map_select_screen(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.select_controls(event.key):
                    self.map_selected = self.map_buttons[self.button_pos[0] + self.button_pos[1]*4]
                    self.current_screen += 1
        self.draw_select_boxes(False)

    def map_carousel_select_screen(self, events):
        for event in events: 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.current_map += 1
                if event.key == pygame.K_LEFT:
                    self.current_map -= 1
        self.draw_map_boxes(self.current_map)
                    

    

    def fight_screen(self):
        self.game_screen.fill(BLUE)

    def draw_select_boxes(self, char: bool):
        self.game_screen.blit(self.select_screen_background, self.select_screen_background.get_rect())
        x = 100
        y = 150
        for i in range(3):
            for j in range(4):
                self.rect.x = x
                self.rect.y = y
                if i == self.button_pos[1] and j == self.button_pos[0]:
                    pygame.draw.rect(self.game_screen, (0, 0, 255), self.rect)
                pygame.draw.rect(self.game_screen, (0, 255, 0), self.rect, 3)
                if char:
                    text_surface = self.font.render(self.char_buttons[(i*4) + j], True, (0, 255, 0))
                    self.game_screen.blit(pygame.image.load(os.path.join('char_select_img', 'IMG_878' + str(i + 1) + '.gif')), self.rect)
                else:
                    text_surface = self.font.render(self.map_buttons[(i*4) + j], True, (0, 255, 0))
                    self.game_screen.blit(pygame.image.load(os.path.join('char_select_img', 'IMG_878' + str(i + 1) + '.gif')), self.rect)
                text_rect = text_surface.get_rect(center=self.rect.center)
                self.game_screen.blit(text_surface, text_rect)
                x += 150
            x = 100
            y += 150
    
    def draw_map_boxes(self, cur_map):
        self.game_screen.fill(BLACK)
        rect_left = pygame.Rect(50, 250, 120, 80)
        rect_middle = pygame.Rect(250, 200, 300, 200)
        rect_right = pygame.Rect(630, 250, 120, 80)
        pygame.draw.rect(self.game_screen, self.map_testing[cur_map - 1], rect_left)
        self.game_screen.blit(pygame.image.load(os.path.join('Backgrounds', self.map_backgrounds[cur_map -1])))
        pygame.draw.rect(self.game_screen, self.map_testing[cur_map], rect_middle)

        self.game_screen.blit(pygame.image.load(os.path.join('Backgrounds', self.map_backgrounds[cur_map])))
        pygame.draw.rect(self.game_screen, self.map_testing[cur_map + 1], rect_right)

        self.game_screen.blit(pygame.image.load(os.path.join('Backgrounds', self.map_backgrounds[cur_map + 1])))


    def select_controls(self, key):
        if key == pygame.K_DOWN:
            self.button_pos[1] += 1
        elif key == pygame.K_UP:
            self.button_pos[1] -= 1
        elif key == pygame.K_RIGHT:
            self.button_pos[0] += 1
        elif key == pygame.K_LEFT:
            self.button_pos[0] -= 1

        if key == pygame.K_RETURN:
            return True

        if self.button_pos[0] < 0:
            self.button_pos[0] = 3
        else:
            self.button_pos[0] = abs(self.button_pos[0])%4
        self.button_pos[1] = self.button_pos[1]%3
        return False