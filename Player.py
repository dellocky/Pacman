# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 18:56:35 2023

@author: footb
"""


from Set_Up import *
#import Debug
import CSV
import Sprite

class Player(Sprite.Sprite):
    def __init__(self, pos, obstacle_sprites, object_sprites):
        #print(pos)
        super().__init__("Player", pos, (TILE_SIZE/2))
        
        self.image_dict= CSV.import_folder_dict('Assets/Pacman Model', (TILE_SIZE*1.25, TILE_SIZE*1.25))
        self.image = self.image_dict["Player Left"]
        self.last_direction='Left'
        
        self.empowered = False

        self.vector = (0, 0)
        self.speed = .575

        self.obstacle_sprites = obstacle_sprites
        self.enemy_sprites = None
        self.object_sprites = object_sprites

        self.animation_time=0
        self.empowered_time = 0
    
    
    def get_enemies(self, enemy_sprites):
        self.enemy_sprites = enemy_sprites
        
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vector = (0, -1)
            self.last_direction = 'Up'
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vector = (0, 1)
            self.last_direction = 'Down'
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vector = (1, 0)
            self.last_direction = 'Right'
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vector = (-1, 0)
            self.last_direction = 'Left'

        #Debug.highlight_hitbox(self.hitbox_rect, self.image, "green")
        
    

    def animate_tic(self):

        self.animation_time += 1
        if self.animation_time<10:
            self.image = self.image_dict[f"Player {self.last_direction}"]

        elif self.animation_time<20:
            if self.vector == (0, 0):
                self.image = self.image_dict[f"Player {self.last_direction}"]
                self.animation_time = 0
            
            else:
                self.image = self.image_dict["Player Full"]
        
        if self.animation_time>=20:
            self.animation_time=0



    def wall_collision(self, vector):
        if vector[0] !=0:
            for sprite in self.obstacle_sprites:
                if sprite.hitbox_rect.colliderect(self.hitbox_rect):
                    #self.canmove=False
                    if self.vector[0] < 0:
                         self.hitbox_rect.left = sprite.hitbox_rect.right
                         self.pos = (self.hitbox_rect.topleft[0]-TILE_SIZE/4,self.hitbox_rect.topleft[1]-TILE_SIZE/4)
                         self.vector = (0, 0)

                    if self.vector[0] > 0:
                         self.hitbox_rect.right = sprite.hitbox_rect.left
                         self.pos = (self.hitbox_rect.topleft[0]-TILE_SIZE/4,self.hitbox_rect.topleft[1]-TILE_SIZE/4)
                         self.vector = (0, 0)

        if vector[1] != 0:
            for sprite in self.obstacle_sprites:
                if sprite.hitbox_rect.colliderect(self.hitbox_rect):
                    #self.canmove=False
                    if self.vector[1] < 0:
                        self.hitbox_rect.top = sprite.hitbox_rect.bottom
                        self.pos = (self.hitbox_rect.topleft[0]-TILE_SIZE/4,self.hitbox_rect.topleft[1]-TILE_SIZE/4)
                        self.vector = (0, 0)

                    if self.vector[1] > 0:
                        self.hitbox_rect.bottom = sprite.hitbox_rect.top
                        self.pos = (self.hitbox_rect.topleft[0]-TILE_SIZE/4,self.hitbox_rect.topleft[1]-TILE_SIZE/4)
                        self.vector = (0, 0)


    def object_collision(self):
        for sprite in self.object_sprites:
            if sprite.hitbox_rect.colliderect(self.hitbox_rect):
                self.object_sprites.remove(sprite)
                if sprite.name == 'Power Pellet 1':
                    self.empowered_time = FPS * 10
                    self.empowered = True
                    for enemy in self.enemy_sprites:
                        enemy.initiate_flee()
    
    
    def empowered_time_tic(self):
        if self.empowered:
            if self.empowered_time > 0:
                self.empowered_time -= 1
            else: 
                self.empowered = False
                for enemy in self.enemy_sprites:
                    enemy.end_flee()
                   
    
    def enemy_collision(self):
        for enemy in self.enemy_sprites:
            if enemy.hitbox_rect.colliderect(self.hitbox_rect):
                if enemy.AI_mode == 'Flee':
                    enemy.initiate_eaten()
                elif enemy.AI_mode == 'Eaten':
                    return
                #else: print("die")
                

    def tic(self):

        self.animate_tic()
        self.empowered_time_tic()

    def collide(self):
        self.object_collision()
        self.wall_collision(self.vector)
        self.enemy_collision()

    def update(self):
        self.input()
        self.tic()
        self.move(self.speed)
        self.collide()
        self.draw()

        

        

