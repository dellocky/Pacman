# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 17:23:19 2023

@author: footb
"""

import pygame
import CSV
from Set_Up import *
from Wall_Sprite import Tile
from Player import Player
from Debug import debug
from Enemy import Enemy
from SpriteGroup import SpriteGroup

class Level:

    def __init__(self):
        
        self.display_surface = pygame.display.get_surface()
        
        self.visible_sprites = []
        self.obstacle_sprites_ai = []
        self.obstacle_sprites_player = []
        self.pickup_sprites = []
        self.wall_sprites = SpriteGroup()
        self.enemy_sprites = SpriteGroup()

        self.is_ticking = True

        self.create_map()
        
    def create_map(self):
        layouts = {
            'Walls' : CSV.csv_layout('Map Layout/PacMan Layout_Walls.csv'),
            'Objects' : CSV.csv_layout('Map Layout/PacMan Layout_Objects.csv'),
            'Gate' : CSV.csv_layout('Map Layout/PacMan Layout_Gate.csv')
        }

        graphics = {
            'Walls': CSV.import_folder_list_dict('Assets/Wall Pieces'),
            'Objects': CSV.import_folder_list_dict('Assets/Pellets'),
            'Gate': CSV.import_folder_list_dict('Assets/Gate'),
            
        }
        

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                      x = col_index * TILE_SIZE
                      y = row_index * TILE_SIZE
                      if style == 'Walls':
                            surf = graphics['Walls'][int(col)][0]
                            Current_Tile=Tile(graphics['Walls'][int(col)][1],(x,y),(col_index, row_index),[self.visible_sprites,self.obstacle_sprites_ai, self.obstacle_sprites_player],'Walls',surf)
                            self.wall_sprites.append(Current_Tile)

                      if style == 'Objects':

                            surf = graphics['Objects'][int(col)][0]
                            Current_Tile=Tile(graphics['Objects'][int(col)][1],(x, y),(col_index, row_index),[self.visible_sprites, self.pickup_sprites], 'Objects', surf)
                            self.wall_sprites.append(Current_Tile)
                        

                      if style == 'Gate':
                             surf = graphics['Gate'][int(col)][0]
                             Current_Tile=Tile(graphics['Gate'][int(col)][1], (x, y),(col_index, row_index),[self.visible_sprites, self.obstacle_sprites_player], 'Gate', surf)
                             self.wall_sprites.append(Current_Tile)


        self.player = Player((TILE_SIZE*13, TILE_SIZE*26), self.obstacle_sprites_player, self.pickup_sprites)

        Ghosts = CSV.get_folder_names('Assets/Ghosts')
       
        for Ghost in Ghosts:
             self.enemy_sprites.append(Enemy(Ghost, [self.visible_sprites, self.enemy_sprites], self.player, self.obstacle_sprites_player, self.enemy_sprites))
        self.player.get_enemies(self.enemy_sprites)

        
    

    def run(self):

        if  self.is_ticking:
            self.player.update()
            self.wall_sprites.update()
            self.enemy_sprites.update()
       
        
        

      
