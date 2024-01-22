# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 17:08:45 2023

@author: footb
"""

import pygame 
from Set_Up import *

    
class Tile(pygame.sprite.Sprite):
    def __init__(self, identifier, pos, groups, sprite_type, surface = pygame.Surface((TILE_SIZE, TILE_SIZE))):
        super().__init__(groups)

        self.identifier = identifier
        self.image = surface
        self.sprite_type = sprite_type
        self.rect = self.image.get_rect(topleft = pos)
        self.coordinates = (round(pos[0] / TILE_SIZE, 0), round(pos[1] / TILE_SIZE, 0))
        self.hitbox = self.rect


        self.animation_time = 0

        if self.sprite_type == 'Walls':
            #test

            self.hitbox.y -= 6
            self.hitbox.x -= 6
            """
            highlight = pygame.Surface(self.hitbox.size)
            highlight.fill((255, 255, 0))
            highlight.set_alpha(128)
            self.image.blit(highlight, (0, 0))
            """

        if  self.sprite_type == 'Gate':
            self.hitbox.y -= 6
            self.hitbox.x -= 6


        if self.sprite_type == 'Objects':
            self.hitbox = self.rect.inflate(-4, -4)
            self.rect = self.hitbox

    def animate_power_pelete(self):
        self.animation_time+=1
        if self.animation_time < 60:
            self.image = pygame.image.load('Assets/Pellets/Power Pellet.png').convert_alpha()
        elif self.animation_time < 120:
            self.image = pygame.image.load('Assets/Pellets/More Pellets/Power Pellet 2.png').convert_alpha()
        else: self.animation_time=0


    def update(self):
        if self.identifier == '1':
            self.animate_power_pelete()




