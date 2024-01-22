# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 17:23:19 2023

@author: footb
"""

#import pygame
import CSV
from Set_Up import *
from Wall_Sprite import Tile
from Player import Player
from Debug import debug
from Enemy import Enemy

class Level:

    def __init__(self):
        
        self.display_surface = pygame.display.get_surface()
        
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites_ai = pygame.sprite.Group()
        self.obstacle_sprites_player = pygame.sprite.Group()
        self.enemy_sprites=pygame.sprite.Group()
        self.pickup_sprites = pygame.sprite.Group()
        
        self.create_map()
        
    def create_map(self):
        layouts = {
            'Walls' : CSV.csv_layout('Map Layout/PacMan Layout_Walls.csv'),
            'Objects' : CSV.csv_layout('Map Layout/PacMan Layout_Objects.csv'),
            'Gate' : CSV.csv_layout('Map Layout/PacMan Layout_Gate.csv')
        }

        graphics = {
            'Walls': CSV.import_folder('Assets/Wall Pieces'),
            'Objects': CSV.import_folder('Assets/Pellets'),
            'Gate': CSV.import_folder('Assets/Gate'),
        }


        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                      x = col_index * TILE_SIZE
                      y = row_index * TILE_SIZE
                      if style == 'Walls':
                            surf = graphics['Walls'][int(col)]
                            Tile('Wall',(x,y),[self.visible_sprites ,self.obstacle_sprites_ai, self.obstacle_sprites_player],'Walls',surf)

                      if style == 'Objects':

                            surf = graphics['Objects'][int(col)]
                            Tile((col),(x, y), [self.visible_sprites, self.pickup_sprites], 'Objects', surf)

                      if style == 'Gate':
                             surf = graphics['Gate'][int(col)]
                             Tile('Gate', (x, y), [self.visible_sprites, self.obstacle_sprites_player], 'Gate', surf)


        self.player = Player((TILE_SIZE*13, TILE_SIZE*26),[self.visible_sprites], self.obstacle_sprites_player, self.pickup_sprites)
        self.blinky = Enemy('Blinky',(TILE_SIZE*13.33, TILE_SIZE*14), [self.visible_sprites, self.enemy_sprites], self.player, self.obstacle_sprites_ai)

                
    def run(self):

        debug(self.blinky.instant_target_point)
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()

