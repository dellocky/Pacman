import pygame
import CSV
import AI_Calculations
from Set_Up import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, identifier, pos, groups, player, obstacle_sprites):
        super().__init__(groups)

        self.identifier = identifier

        self.pos = pos
        self.coordinates = (round(pos[0] / TILE_SIZE, 0), round(pos[1] / TILE_SIZE, 0))
        self.delay = 0

        self.groups = groups

        self.player = player
        self.player_point = self.player.coordinates
        self.target_point = None

        if identifier == 'Blinky':
            self.instant_target_point = (12,14)

        self.image_list = CSV.import_folder(f'Assets/Ghosts/{self.identifier}')
        self.image = self.image_list[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.image = pygame.transform.smoothscale(self.image, (20, 20))

        self.potential_directions = []
        self.direction = (-1, 0)
        self.speed = .675

        self.obstacle_sprites = obstacle_sprites

    def update_coordinates(self):
        self.coordinates = (round(self.pos[0] / TILE_SIZE, 0), round(self.pos[1] / TILE_SIZE, 0))
    def move(self, speed):

        self.pos = (self.pos[0] + self.direction[0] * speed, self.pos[1] + self.direction[1] * speed)
        self.rect.topleft = self.pos
        self.update_coordinates()



    def acquire_target(self):

        self.player_point = self.player.coordinates
        if self.identifier == 'Blinky':
            self.target_point = self.player_point

    def direction_turner(self):

            self.direction = AI_Calculations.direction_turner(self.coordinates, self.instant_target_point)

        #print(self.instant_target_point)

    def tile_check(self):

        potential_tiles = AI_Calculations.remove_opposite_direction(AI_Calculations.neighbor_tile_calculator(self.coordinates), self.direction)
        for index, coordinate in  enumerate (potential_tiles):
            for sprite in self.obstacle_sprites:
                if sprite.coordinates == coordinate:
                    del(potential_tiles[index])


        selected_tile=AI_Calculations.distance_calculator(potential_tiles, self.player.coordinates)

        self.instant_target_point = selected_tile
        self.direction_turner()


    def update(self):

        self.acquire_target()
        if self.instant_target_point == self.coordinates:
            self.tile_check()
        self.move(self.speed)

