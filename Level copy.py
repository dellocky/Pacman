# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 17:23:19 2023

@author: footb
"""

import pygame
import CSV
from Set_Up import *
from Tile import Tile
from Object_Sprite import Object_Sprite
from Player import Player
from Debug import debug
from Enemy import Enemy
from SpriteGroup import SpriteGroup

class Level:

    def __init__(self):
        
        self.display_surface = pygame.display.get_surface()
    
        self.obstacle_sprites = SpriteGroup('obstacle_sprites')
        self.wall_sprites = SpriteGroup('wall_sprites')
        self.object_sprites = SpriteGroup('object_sprites')
        self.enemy_sprites = SpriteGroup('enemy_sprites')

        self.tile_map = {}

        self.is_ticking = True

        self.create_tiles()
        self.create_map()

    #turns X and Y corrdinates into objects for pathfinding
    def create_tiles(self):
    

        x = 0
        y = 0
        for tiles in  range (HEIGHT):
            for tile in range (WIDTH):
                self.tile_map[(x, y)] = Tile((x, y))
                x += 1
            y += 1
            x = 0
        
    #attaches sprites to tiles based off the coordinates as well as creating moving sprites
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
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE
                    if col != '-1':
                      if style == 'Walls':
                            surf = graphics['Walls'][int(col)][0]
                            self.tile_map[col_index, row_index].sprite = Object_Sprite(graphics['Walls'][int(col)][1],(x,y),[self.obstacle_sprites, self.wall_sprites], TILE_SIZE*.9,surf)
                            self.tile_map[col_index, row_index].wall = True
                      if style == 'Objects':

                            surf = graphics['Objects'][int(col)][0]
                            self.tile_map[col_index, row_index].sprite = Object_Sprite(graphics['Objects'][int(col)][1],(x, y),[self.object_sprites], TILE_SIZE*.5, surf)
                            
                      if style == 'Gate':
                             surf = graphics['Gate'][int(col)][0]
                             self.tile_map[col_index, row_index].sprite = Object_Sprite(graphics['Gate'][int(col)][1], (x, y),[self.obstacle_sprites, self.wall_sprites], TILE_SIZE*.75, surf)
                             self.tile_map[col_index, row_index].wall = True
        
        self.flag_map = []
        current_row = []
        count = 0
        for tile in self.tile_map.values():
            if tile.wall:
                current_row.append(True)
            else:
                current_row.append(False)
            count += 1
            if count == WIDTH:
                self.flag_map.append(current_row)
                current_row = list()
                count = 0
     
        self.player = Player((TILE_SIZE*13, TILE_SIZE*26), self.obstacle_sprites, self.object_sprites)

        Ghosts = CSV.get_folder_names('Assets/Ghosts')
       
        for Ghost in Ghosts:
            Enemy(Ghost, [self.enemy_sprites], self.player, self.obstacle_sprites, self.tile_map, self.flag_map)
        self.player.get_enemies(self.enemy_sprites)

    #main loop feed
    def run(self):

        if  self.is_ticking:
            self.player.update()
            self.wall_sprites.update()
            self.object_sprites.update()
            self.enemy_sprites.update()

        for tile in self.tile_map.values():
            if tile.draw:
                tile.drawer()
            
       
       
        
        

      
