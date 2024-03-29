import os
import pygame
#the first parameter is the powerup. the second parameter is the damage it does  
character_powerups = {
            "Ryu": ["Fireball", 9], 
            "Balrog": ["Strong Kick", 9], 
            "Blanka": ["Energized Attack", 9], 
            "Dhalsim": ["Fury Fire", 7],  
            "Sagat":  ["Rapid Hit", 12],  
            "Guile": ["Flash Punch", 10], 
            "Vega": ["Super Claw Attack", 11], 
            "Chun Li": ["Power Punch", 8],  
            "Zangief": ["Lariat", 9], 
            "E Honda": ["Super Kick", 9], 
            "M Bison": ["Super Strength", 11], 
            "Ken": ["Lightning Kick", 13]
        }


  # formatted as [punch, kick]
character_damage_values = {
            "Ryu": [7, 10],
            "Balrog": [8, 7],
            "Blanka": [7, 8],
            "Dhalsim": [5, 11],
            "Sagat":  [10, 6],
            "Guile": [8, 8],
            "Vega": [9, 7],
            "Chun Li": [6, 9],
            "Zangief": [7, 7],
            "E Honda": [9, 7],
            "M Bison": [9, 6],
            "Ken": [7, 11]
}


class playerState(pygame.sprite.Sprite):
    def __init__(self, champion: str, isPlayer2 = False):
        pygame.sprite.Sprite.__init__(self)
        self.cur_type_animation = "idle"
        self.champion = champion
        self.hp = 100
        self.isBlocking = False
        self.isAttacking = False
        self.landed_hit = False
        self.attackValue = character_damage_values[self.champion]
        self.MIN_HP_NUM = 0
        self.champions_background_color = {"Balrog": [0, 0, 0], "Blanka": [], "ChunLi": [], "Dhalsim": [32, 144, 160], "E Honda": [], "Guile": [], "Ken": [128, 184, 168], "M Bison": [], "Ryu": [], "Sagat": [], "Vega":[], "Zangief": []}
        self.champAnimations = {"walk": [], "idle": [], "basic kick": [], "basic punch": [], "crouch": [], "jump": []}
        self.cur_pressed_keys = {"left": False, "right": False, "down": False, "kick": False, "punch": False, "powerup": False}
        self.jump = False
        self.velocity = 0
        self.character_powerup_name = None
        self.isPlayer2 = isPlayer2
        self.same_initial_direction = True
        self.use_power_up = False
        self.cur_frame = 0
        self.load_animations()
        self.image = self.champAnimations["idle"][0]
        self.rect = self.image.get_rect()
        if isPlayer2:
            self.rect.x += 700
        else:
            self.rect.x += 50
        self.rect.y += 350
        
    
    def load_animations(self):
        
        """Will load the animations for the current champion into 
            champAnimations, and populate the dictinonary"""
        #for x in self.champAnimations.keys():
        for y in range(len(os.listdir(os.path.join('Character_images', f'{self.champion}', 'walk')))):
            image = pygame.image.load(os.path.join('Character_images', f'{self.champion}', 'walk', f'{y}.png'))
            if self.isPlayer2:
                 image = pygame.transform.flip(image, True, False)
            self.champAnimations[f"walk"].append(image)
        
        for x in range(len(os.listdir(os.path.join('Character_images', f'{self.champion}', 'idle')))):
            image = pygame.image.load(os.path.join('Character_images', f'{self.champion}', 'idle', f'{x}.png'))
            if self.isPlayer2:
                 image = pygame.transform.flip(image, True, False)
            self.champAnimations[f"idle"].append(image)

        for u in range(len(os.listdir(os.path.join('Character_images', f'{self.champion}', 'basic punch')))):
            image = pygame.image.load(os.path.join('Character_Images',f'{self.champion}','basic punch',f'{u}.png'))
            if self.isPlayer2:
                image = pygame.transform.flip(image,True,False)
            self.champAnimations[f"basic punch"].append(image)
        
        for z in range(len(os.listdir(os.path.join('Character_images', f'{self.champion}', 'jump'))) - 1):
            image = pygame.image.load(os.path.join('Character_images', f'{self.champion}', 'jump', f'{z}.png'))
            if self.isPlayer2:
                 image = pygame.transform.flip(image, True, False)
            image.convert_alpha()
            self.champAnimations[f"jump"].append(image)

        for w in range(len(os.listdir(os.path.join('Character_images', f'{self.champion}', 'crouch'))) - 1):
            image = pygame.image.load(os.path.join('Character_Images',f'{self.champion}','crouch',f'{w}.png'))
            if self.isPlayer2:
                image = pygame.transform.flip(image,True,False)
            image.convert_alpha()
            self.champAnimations[f"crouch"].append(image)
            
        for v in range(len(os.listdir(os.path.join('Character_images', f'{self.champion}', 'basic kick'))) - 1):
            image = pygame.image.load(os.path.join('Character_Images',f'{self.champion}','basic kick',f'{v}.png'))
            if self.isPlayer2:
                image = pygame.transform.flip(image,True,False)
            image.convert_alpha()
            self.champAnimations[f"basic kick"].append(image)
            
            
                    
        
    
    def update(self):
        if self.isAttacking == False:
            if self.cur_pressed_keys["left"]:
                    self.rect.x += -5
                    self.cur_frame += 1
                    if self.cur_frame/5 >= len(self.champAnimations["walk"]):
                        self.cur_frame = 0
                    self.image = self.champAnimations["walk"][self.cur_frame//5]
                    if self.isPlayer2 != True:
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.same_initial_direction = False
                    elif self.isPlayer2 == True:
                        self.same_initial_direction = True
            elif self.cur_pressed_keys["right"]:
                    self.rect.x += 5
                    self.cur_frame += 1
                    if self.cur_frame/5 >= len(self.champAnimations["walk"]):
                        self.cur_frame = 0
                    self.image = self.champAnimations["walk"][self.cur_frame//5]
                    if self.isPlayer2:
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.same_initial_direction = False
                    elif self.isPlayer2 != True:
                        self.same_initial_direction = True
            else:
                if self.cur_frame/5 >= len(self.champAnimations["idle"]):
                        self.cur_frame = 0
                self.image = self.champAnimations["idle"][self.cur_frame//5]
                if self.same_initial_direction != True:
                     self.image = pygame.transform.flip(self.image, True, False)
                self.cur_type_animation = "idle"
        else:
            if self.cur_type_animation == 'punch':
                self.cur_frame += 1
                if self.cur_frame/5 >= len(self.champAnimations["basic punch"]):
                    self.cur_frame = 0
                    self.isAttacking = False
                    self.landed_hit = False
                self.image = self.champAnimations["basic punch"][self.cur_frame//5]  
                #check for collison between two sprites and check if the charcter that got attacked is blocking or not 
                #then update their hp using 
                if self.same_initial_direction != True: #making sure you know what direction playertwo is facing in 
                    self.image = pygame.transform.flip(self.image, True, False)
                #self.attackValue = self.updateHp(character_damage_values[self.champion][0])
            if self.cur_type_animation == "kick":
                #self.attackValue = self.updateAttackVal(self.champion)
                self.cur_frame += 1
                if self.cur_frame/5 >= len(self.champAnimations["basic kick"]):
                    self.cur_frame = 0
                    self.isAttacking = False
                    self.landed_hit = False
                self.image = self.champAnimations["basic kick"][self.cur_frame//5]  
                #check for collison between two sprites and check if the charcter that got attacked is blocking or not 
                #then update their hp using 
                if self.same_initial_direction != True: #making sure you know what direction playertwo is facing in 
                    self.image = pygame.transform.flip(self.image, True, False)
                #self.attackValue = self.updateHp(character_damage_values[self.champion][0])
            #when doing anything with attackValue, use the updateAttackVal, 
    def getPosition(self):
        return self.rect

    def updateHp(self, attackVal):
        if self.isBlocking == False:
             self.hp -= attackVal

        """Will update the amount of health remaining based on
            the attack the user was hit with  

        Args:
            attack (_type_): _description_
        """
    def getPowerupInfo(self, champion, index): 
        return character_powerups[champion][index]
    
    def setAttackVal(self, champion, isKick, player_powerup = None): 
        if isKick and character_damage_values[champion][1] ==  character_damage_values[champion][1] + player_powerup:
            character_damage_values[champion][1] = character_damage_values[champion][1]; 
        elif not isKick and character_damage_values[champion][0] == character_damage_values[champion][0] + player_powerup: 
            character_damage_values[champion][0] = character_damage_values[champion][0]; 
        else: 
            if isKick:
                character_damage_values[champion][1] += player_powerup 
            else:
                character_damage_values[champion][0] += player_powerup

        return "Player powered up"

    def resetAttackVal(self, champion, isKick, player_powerup):
        if isKick: 
            character_damage_values[champion][1] -= player_powerup
        else: 
            character_damage_values[champion][0] -= player_powerup 
        
        return "Player attack reset"
        
    def updateAttackVal(self, champion):
        self.attackValue = character_damage_values[champion]     