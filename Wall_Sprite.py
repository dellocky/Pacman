# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 17:08:45 2023

@author: footb
"""

import pygame 
from Set_Up import *
import Debug

    
class Tile():
    def __init__(self, identifier, pos, coordinates, groups, sprite_type, surface = pygame.Surface((TILE_SIZE, TILE_SIZE))):

        self.identifier = identifier
        self.image = surface
        self.sprite_type = sprite_type
        self.pos = pos
        self.hitbox_rect = pygame.Rect(pos[0],pos[1],12,12)
        self.hitbox_rect.center = (self.pos[0]+(TILE_SIZE/2),self.pos[1]+(TILE_SIZE/2))
        self.coordinates = coordinates
        self.display = pygame.display.get_surface()
        self.animation_time = 0
        self.exists = True

        for I in groups:
            I.append(self)
            
        self.preload()
        

    def preload(self):
        
        
        if self.identifier == '1':
            self.power_pellet_image1 = pygame.image.load('Assets/Pellets/Power Pellet.png').convert_alpha()
            self.power_pellet_image2 = pygame.image.load('Assets/Pellets/More Pellets/Power Pellet 2.png').convert_alpha()



    def animate_power_pelete(self):
            
            if self.identifier == '1':
                self.animation_time+=1
                if self.animation_time < 65:
                    self.image = self.power_pellet_image1
                elif self.animation_time < 130:
                    self.image = self.power_pellet_image2
                else: self.animation_time=0

    def drawer(self):
        if self.exists:
            self.display.blit(self.image, (self.pos))
            #pygame.draw.rect(self.display, (255,0,0), self.hitbox_rect)

    def kill(self):

        self.exists = False

    def update(self):

        self.animate_power_pelete()
        self.drawer()
        
   



