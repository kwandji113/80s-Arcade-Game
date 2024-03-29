import pygame
import os
from StartScreen import StartScreen
from ChampionSelectScreen import ChampionSelectScreen
from MapSelectScreen import MapSelectScreen
from playerone import player1
from playertwo import player2
from GameOverScreen import GameOverScreen
from transition import transition

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255,0,0); 
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

class screenState():
    
    def __init__(self, game_screen) -> None:
        self.game_screen = game_screen
        self.current_screen = 0
        self.map_selected = None
        self.map_image = None
        pygame.mixer.music.load(os.path.join('music', "Opening Demo.mp3"))
        pygame.mixer.music.play(-1)
        self.rect = pygame.Rect(100, 150, 120, 100)
        self.screens = []
        self.num_char_selected = 0
        self.chars_selected = []
        self.players = pygame.sprite.Group()
        self.is_zoomed_in = True
        self.winner = None
        self.players_position = {'player1': pygame.Rect, 'player2': pygame.Rect}
        self.transition = transition()
        self.startScreen = StartScreen(self.game_screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.champSelectScreen = ChampionSelectScreen(self.game_screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.mapSelectScreen = MapSelectScreen(self.game_screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player_that_won = 5
        self.p1_powerup_box_color = BLUE
        self.p2_powerup_box_color = BLUE 
    
    def update_screen(self, events):
        if self.current_screen == 0:
            if self.startScreen.update(events):
                self.transition.reset()
                pygame.mixer.music.fadeout(2)
                pygame.mixer.music.load(os.path.join('music', 'Player Select.mp3'))
                pygame.mixer.music.play(-1)
        elif self.current_screen == 1:
            self.chars_selected = self.champSelectScreen.update(events)
            if self.chars_selected != None:
                for x in self.chars_selected:
                    self.players.add(x)
                self.transition.reset()
        elif self.current_screen == 2:
            self.map_selected = self.mapSelectScreen.update(events)
            self.champSelectScreen.draw_selected_characters()
            if self.map_selected != None:
                self.map_image = pygame.transform.scale(pygame.image.load(os.path.join('Backgrounds', f"{self.map_selected}.png")), (1200, SCREEN_HEIGHT))
                self.transition.reset()
                pygame.mixer.music.fadeout(2)
                pygame.mixer.music.load(os.path.join('music', 'stage music', f"{self.map_selected}.mp3"))
                pygame.mixer.music.play(-1)
        elif self.current_screen == 3:
            self.fight_screen(events)
        elif self.current_screen == 4:
            self.game_over_screen(events)
        if self.transition.fading != None:
            self.transition.draw(self.game_screen)
            if self.transition.update():
                self.current_screen += 1
        

    def fight_screen(self, events):
        # image, (xcoordtobeplaced, ycoordtobeplaced), xcoordtostartcutting, ycoordtostartcutting, lenofimage, heightofimage
        
        self.move_fight_border()
        self.player_out_of_bounds() #pygame.sprite.players.sprites()
        self.players.update(events)
        sprites = self.players.sprites()
        for x in sprites:
            if x.isAttacking and x.landed_hit != True:
                if pygame.sprite.collide_rect(sprites[0], sprites[1]):
                    if x.isPlayer2 != True:
                        #check for punch or kick
                        if x.cur_type_animation == 'punch':
                            sprites[1].updateHp(x.attackValue[0])
                            sprites[0].landed_hit = True
                            if sprites[1].hp <= 0:
                                return 1
                        if x.cur_type_animation == 'kick':
                            sprites[1].updateHp(x.attackValue[1])
                            sprites[0].landed_hit = True
                            if sprites[1].hp <= 0:
                                return 1
                    else:
                        if x.cur_type_animation == 'punch':
                            sprites[0].updateHp(x.attackValue[0])
                            sprites[1].landed_hit = True
                            if sprites[0].hp <= 0:
                                return 2
                        if x.cur_type_animation == 'kick':
                            sprites[0].updateHp(x.attackValue[1])
                            sprites[1].landed_hit = True
                            if sprites[0].hp <= 0:
                                return 2
        self.players.draw(self.game_screen)

        p1 = self.draw_powerup_box(self.p1_powerup_box_color, (30,90,50,50)) 
        p2 = self.draw_powerup_box(self.p2_powerup_box_color, (560, 90, 50,50))

        for event in events: 
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_c):
                if self.p1_powerup_box_color == (0,255,255): 
                    i = 0
                    while i < 5: 
                        None
                        i += 1
                    self.p1_powerup_box_color = (255,0,0)
                else: 
                    self.p1_powerup_box_color = (255,0,0); 
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_l): 
                if self.p2_powerup_box_color == (0,255,255): 
                    i = 0
                    while i < 5: 
                        None
                        i += 1
                    self.p2_powerup_box_color = (255,0,0)
                else: 
                    self.p2_powerup_box_color = (255,0,0); 
        



                          
        player1 = self.players.sprites()[0]
        player2 = self.players.sprites()[1]

        # if player1.isAttacking:
	    #     player2.updateHp(player1.attackVal)
        
        # health bar
        player1_hp = self.players.sprites()[0].hp
        player2_hp = self.players.sprites()[1].hp
        pygame.draw.rect(self.game_screen, (0, 0, 0), (30, 20, 210, 50), 5)
        self.update_player_health(player1_hp, 1)

        pygame.draw.rect(self.game_screen, (0, 0, 0), (560, 20, 210, 50), 5)
        self.update_player_health(player2_hp, 2)

        if player1_hp <= 0:
            self.transition.reset()
            pygame.mixer.music.fadeout(2)
            pygame.mixer.music.load(os.path.join('music', 'Game Over.mp3'))
            self.player_that_won = 2
        if player2_hp <= 0:
            self.transition.reset()
            pygame.mixer.music.fadeout(2)
            pygame.mixer.music.load(os.path.join('music', 'Game Over.mp3'))
            self.player_that_won = 1


    def move_fight_border(self):
        # map_image = pygame.transform.scale(pygame.image.load(os.path.join('Backgrounds', self.map_backgrounds[self.map_selected])), SCREEN_SIZE)
        # self.game_screen.blit(map_image, self.select_screen_background.get_rect())
        player_list = self.players.sprites()
        left_border = (player_list[0].rect.x+player_list[1].rect.x)/2

        if left_border < 0:
            left_border = 0
        elif left_border > 390:
            left_border = 390
        if self.is_zoomed_in:
            self.game_screen.blit(self.map_image, (0, 0), (left_border, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        else: 
            self.game_screen.blit(self.map_image, (0, 0), (200, 0, SCREEN_WIDTH, SCREEN_HEIGHT))


    def player_out_of_bounds(self):
        player1_x = self.players.sprites()[0].rect.x
        player2_x = self.players.sprites()[1].rect.x
        left_icon_triggered = False
        right_icon_triggered = False

        if player2_x < 0:
            icon = pygame.image.load(os.path.join('Other_images', 'player2_left_outofbounds.png'))
            self.game_screen.blit(icon, pygame.Rect(20, 250, 20, 20))
            left_icon_triggered = True

        elif player2_x > SCREEN_WIDTH:
            icon = pygame.image.load(os.path.join('Other_images', 'player2_right_outofbounds.png'))
            self.game_screen.blit(icon, pygame.Rect(705, 250, 20, 20))
            right_icon_triggered = True

        if player1_x < 0:
            icon = pygame.image.load(os.path.join('Other_images', 'player1_left_outofbounds.png'))
            if left_icon_triggered:
                self.game_screen.blit(icon, pygame.Rect(20, 160, 20, 20))
            else:
                self.game_screen.blit(icon, pygame.Rect(20, 250, 20, 20))
            left_icon_triggered = True

        elif player1_x > SCREEN_WIDTH:
            icon = pygame.image.load(os.path.join('Other_images', 'player1_right_outofbounds.png'))
            if right_icon_triggered:
                self.game_screen.blit(icon, pygame.Rect(705, 160, 20, 20))
            else:
                self.game_screen.blit(icon, pygame.Rect(705, 250, 20, 20))
            right_icon_triggered = True
            
    def update_player_health(self, health, player_number):
        health_color = None
        if health > 70:
            health_color = (0, 255, 0)
        elif health > 30:
            health_color = (255, 255, 0)
        else:
            health_color = (255, 0, 0)

        if player_number == 1:
            pygame.draw.rect(self.game_screen, health_color , (35, 25, health * 2, 40))
        else: 
            pygame.draw.rect(self.game_screen, health_color , (SCREEN_WIDTH - health * 2 - 35, 25, health * 2, 40))

    
    def draw_powerup_box(self, color, rect):
        pygame.draw.rect(self.game_screen, color, rect)


    def game_over_screen(self, events):
        game_over_background = pygame.image.load(os.path.join('Backgrounds', "game_over_screen.jpeg"))
        game_over_background = pygame.transform.scale(game_over_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.game_screen.blit(game_over_background, (0,0))
        font = pygame.font.SysFont("ptserif", 70)

        winning_player_text = font.render("Player " + str(self.player_that_won) + " Wins!", 1, (222, 71, 33))
        winning_player_text_pos = winning_player_text.get_rect()
        winning_player_text_pos.center = game_over_background.get_rect().center
        winning_player_text_pos.y -= 120
        self.game_screen.blit(winning_player_text, winning_player_text_pos)

        font = pygame.font.SysFont("ptserif", 50)

        instructions_text = font.render("To Restart Press Space", 1, (222, 146, 33))

        instructions2_text = font.render("To End Game Press Enter", 1, (222, 187, 33))

        instructions_text_pos = instructions_text.get_rect()
        instructions_text_pos.center = game_over_background.get_rect().center
        instructions_text_pos.y += 110

        instructions2_text_pos = instructions2_text.get_rect()
        instructions2_text_pos.center = game_over_background.get_rect().center
        instructions2_text_pos.y += 180

        self.game_screen.blit(instructions_text, instructions_text_pos)
        self.game_screen.blit(instructions2_text, instructions2_text_pos)
        
        self.users_next_steps(events)

    
    def users_next_steps(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP: 
                if event.key == pygame.K_SPACE:
                    self.reset_game()
                if event.key == pygame.K_RETURN:
                    pygame.quit()

    def reset_game(self):
        self.current_screen = 0
        self.map_selected = None
        self.map_image = None
        self.num_char_selected = 0
        self.champSelectScreen.reset()
        self.players = pygame.sprite.Group()
        self.players_position = {'player1': pygame.Rect, 'player2': pygame.Rect}
        self.player_that_won = None
        self.p1_powerup_box_color = BLUE 
        self.p2_powerup_box_color = BLUE
    

        

        

