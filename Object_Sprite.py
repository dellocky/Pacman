# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 17:08:45 2023

@author: footb
"""

import pygame 
from Set_Up import *
#import Debug
import Sprite

    
class Object_Sprite(Sprite.Sprite):

    def __init__(self, name, pos, groups, hitbox_size, surface = pygame.Surface((TILE_SIZE, TILE_SIZE))):
        
        super().__init__(name, pos, hitbox_size, groups)
        self.image = surface
        self.animation_time = 0
        self.preload()

    def preload(self):
        
        if self.name == 'Power Pellet 1':
            self.power_pellet_image1 = pygame.image.load('Assets/Pellets/Power Pellet 1.png').convert_alpha()
            self.power_pellet_image2 = pygame.image.load('Assets/Pellets/Power Pellet 2.png').convert_alpha()

    def animate_power_pelete(self):
            
            if self.name == 'Power Pellet 1':
                self.animation_time+=1
                if self.animation_time < 65:
                    self.image = self.power_pellet_image1
                elif self.animation_time < 130:
                    self.image = self.power_pellet_image2
                else: self.animation_time=0

    def update(self):

        self.animate_power_pelete()
        self.draw()
        
   



