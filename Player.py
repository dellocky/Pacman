# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 18:56:35 2023

@author: footb
"""


from Set_Up import *
import Debug
import CSV

class Player():
    def __init__(self, pos, obstacle_sprites, object_sprites):
        self.pos = pos
        self.coordinates = (round(pos[0] / TILE_SIZE, 0), round(pos[1] / TILE_SIZE, 0))
        self.image_dict= CSV.import_folder_dict('Assets/Pacman Model', (19, 19))
        self.image = self.image_dict["Player Left"]
        self.display = pygame.display.get_surface()
        

        self.hitbox_rect = pygame.Rect(100,100,8,8)
        self.hitbox_rect.center = (self.pos[0]+(TILE_SIZE/2),self.pos[1]+(TILE_SIZE/2))
        self.last_direction='Left'
        self.canmove = True

        self.vector = (0, 0)
        self.speed = .575

        self.obstacle_sprites = obstacle_sprites
        self.enemy_sprites = None
        self.object_sprites = object_sprites

        self.animation_time=0
    
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
    """else:
            self.vector = (0, 0)
            self.animation_time=0
            if self.last_direction == 'up':
                self.image = self.image_dict["Player Up"]
                
            if self.last_direction == 'down':
                self.image = self.image_dict["Player Down"]
                
            if self.last_direction == 'right':
                self.image = self.image_dict["Player Right"]
                
            if self.last_direction == 'left':
                self.image = self.image_dict["Player Left"]
                 """

        #Debug.highlight_hitbox(self.hitbox_rect, self.image, "green")
        
        
    def update_coordinates(self):
        self.coordinates = (round(self.pos[0] / TILE_SIZE, 0), round(self.pos[1] / TILE_SIZE, 0))

    def move(self, speed):
     if self.canmove:
        self.pos = (self.pos[0]+self.vector[0]*speed, self.pos[1]+self.vector[1]*speed)
        self.hitbox_rect.center = (self.pos[0]+(TILE_SIZE/2),self.pos[1]+(TILE_SIZE/2))

        if self.hitbox_rect.x < -12:

            self.pos =(442, self.pos[1])


        elif self.hitbox_rect.x > 448:

            self.pos=(-6, self.pos[1])

        self.update_coordinates()

    def animate(self):
        self.animation_time += 1
        current_image = self.image
        if self.animation_time<10:
            self.image = self.image_dict[f"Player {self.last_direction}"]

        elif self.animation_time<20:
            self.image = self.image_dict["Player Full"]
            

        if self.animation_time>=20:
            self.image=current_image
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
                sprite.kill()

    def enemy_collision(self):
        for sprite in self.enemy_sprites:
            if sprite.hitbox_rect.colliderect(self.hitbox_rect):
                pass

    def drawer(self):
        self.display.blit(self.image, (self.pos))
        #pygame.draw.rect(self.display, (0,0,255), self.hitbox_rect)

    def update(self):
        if self.canmove:
            self.input()
        self.move(self.speed)
        self.object_collision()
        self.wall_collision(self.vector)
        self.enemy_collision()
        self.animate()
        self.drawer()
        

        

