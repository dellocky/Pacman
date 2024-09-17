import pygame
import CSV
import AI_Calculations
import Debug
from Set_Up import *


class Enemy():
    def __init__(self, identifier, groups, player, obstacle_sprites, enemy_sprites):

        self.identifier = identifier
        print 

        if identifier == 'Blinky':
            self.pos = (TILE_SIZE*13.5, TILE_SIZE*14)
            self.instant_target_point = (12,14)
            
            self.vector = (-1, 0)
            self.direction = "Left"
            
            self.AI_mode = "Chase"
            self.spawn_state = 0
            self.spawn_delay_time = 0
            

        elif identifier == 'Pinky':
            self.pos = (TILE_SIZE*13.5, TILE_SIZE*17)
            self.instant_target_point = (14, 16)
            
            self.vector = (0, -1)
            self.direction = "Up"
            
            self.AI_mode = "Spawn"
            self.spawn_state = 0
            self.spawn_delay_time = FPS * 8
         
        
        
        elif identifier == 'Inky':
            self.pos = (TILE_SIZE*11.5, TILE_SIZE*17)
            self.instant_target_point = (12, 18)
            
            self.vector = (0, 1)
            self.direction = "Down"
            
            self.AI_mode = "Spawn"
            self.spawn_state = 0
            self.spawn_delay_time = FPS * 16
           

        
        elif identifier == 'Clyde':
            self.pos = (TILE_SIZE*15.5, TILE_SIZE*17)
            self.instant_target_point = (16, 18)
            
            self.vector = (0, 1)
            self.direction = "Down"
           
            self.AI_mode = "Spawn"
            self.spawn_state = 0
            self.spawn_delay_time = FPS * 24
            

        self.coordinates = (round(self.pos[0] / TILE_SIZE), round(self.pos[1] / TILE_SIZE))

        self.groups = groups
        self.display = pygame.display.get_surface()

        self.player = player
        self.player_point = self.player.coordinates
        self.target_point = None

        self.hitbox_rect = pygame.Rect(100,100,8,8)
        self.hitbox_rect.center = (self.pos[0]+(TILE_SIZE/2),self.pos[1]+(TILE_SIZE/2))
        self.test_rect = None
    
        self.image_dict= CSV.import_folder_dict(f'Assets/Ghosts/{self.identifier}', (19, 19))

        self.potential_directions = []
        self.speed = .575

        self.pos_time = round((TILE_SIZE/2)/self.speed)
        self.pos_countdown = 0
        self.pos_delay_active = False

        self.animation_state = 1
        self.animation_countdown = 0

        self.update_image()

        self.obstacle_sprites = obstacle_sprites
        enemy_sprites.append(self)
            
    def get_blinky(self, enemy_sprites):
        for ghost in enemy_sprites:
            if ghost.identifier == "Blinky":
                pass

    def update_coordinates(self):
        self.coordinates = (round(self.pos[0] / TILE_SIZE, 0), round(self.pos[1] / TILE_SIZE, 0))
    
    def update_image(self):
        self.image = self.image_dict[f"{self.identifier} Eyes {self.direction} {self.animation_state}"]

    def move(self, speed):

        self.pos = (self.pos[0] + self.vector[0] * speed, self.pos[1] + self.vector[1] * speed)
        self.hitbox_rect.center = (self.pos[0]+(TILE_SIZE/2),self.pos[1]+(TILE_SIZE/2))
        self.update_coordinates()

        if self.hitbox_rect.x < -2:

            self.pos =(442, self.pos[1])
            self.instant_target_point = (27, 17)


        elif self.hitbox_rect.x > 448:

            self.pos=(-6, self.pos[1])
            self.instant_target_point = (0, 17)

    def turn(self, vector):
         
        self.vector = vector
        if vector == (1, 0):
             self.direction = "Right"
             self.update_image()
            
        elif vector == (-1, 0):
             self.direction = "Left"
             self.update_image()

        elif vector == (0, 1):
             self.direction = "Down"
             self.update_image()

        elif vector == (0, -1):
             self.direction = "Up"
             self.update_image()

    def aquire_target(self):

        if self.identifier == 'Blinky':
            self.target_point = self.player.coordinates

        if self.identifier == 'Pinky':
            self.target_point = ((self.player.coordinates[0]+self.player.vector[0]*2), (self.player.coordinates[1]+self.player.vector[1]*2))

        if self.identifier == 'Inky':

            self.target_point = ((self.player.coordinates[0]-self.player.vector[0]*2), (self.player.coordinates[1]-self.player.vector[1]*2))
            
        if self.identifier == 'Clyde':

            self.target_point = ((round(self.player.coordinates[0]-self.player.vector[0]*6)), (round(self.player.coordinates[1]-self.player.vector[1]*6)))
        

    def spawn(self):
        
        pass
    
    def direction_flip(self):
         
        self.turn(AI_Calculations.turn_around(self.vector))
        self.instant_target_point = (self.coordinates[0]+(self.vector[0]*2), self.coordinates[1]+(self.vector[1]*2))

    def direction_change(self):


        self.turn(AI_Calculations.direction_turner(self.coordinates, self.instant_target_point))

        

    def navigate(self):

        potential_tiles = AI_Calculations.remove_opposite_direction(AI_Calculations.neighbor_tile_calculator(self.coordinates), self.vector)
        for index, coordinate in  enumerate (potential_tiles):
            for sprite in self.obstacle_sprites:
                if sprite.coordinates == (coordinate[0], coordinate[1]):
                    potential_tiles[index] = (coordinate[0], coordinate[1], False)

        final_tiles=[]
        for tile in potential_tiles:
            if tile[2]:
                final_tiles.append(tile)

        selected_tile= AI_Calculations.distance_calculator(final_tiles, self.target_point)
        self.instant_target_point = (selected_tile[0], selected_tile[1])
        self.direction_change()



    def movement_countdown(self):
        if self.pos_delay_active:
            self.pos_countdown -=1
            #if self.identifier == 'Inky':
                #print(f'Countdown = {self.pos_countdown}\nState = {self.spawn_state}')
            if self.pos_countdown <= 0:
                self.pos_delay_active = False
                self.pos_countdown = self.pos_time
                if self.AI_mode == "Chase":
                    self.navigate()

                if self.AI_mode == "Spawn" and self.spawn_state == 0:
                    self.direction_flip()
                
                elif self.AI_mode == "Spawn" and self.spawn_state == 1:
                    self.spawn_2()

                elif self.AI_mode == "Spawn" and self.spawn_state == 2:
                    self.spawn_3()

                elif self.AI_mode == "Spawn" and self.spawn_state == 3:
                    
                    self.AI_mode = "Chase"
                    self.aquire_target()
                    self.navigate()
                  
                  
                 

        
                
            
    def enemy_collision(self):
           pass
        #if self.player.hitbox_rect.colliderect(self.hitbox_rect):
            #print("test")
    
     
    def spawn_1(self):
        if self.spawn_state == 0:
            self.spawn_state = 1
            if self.coordinates != 14:
                self.instant_target_point = (self.coordinates[0], 17)
                target_pos = ((self.instant_target_point[0]*TILE_SIZE),(self.instant_target_point[1]*TILE_SIZE))
                if self.pos == target_pos:
                    self.spawn_2()
                else:
                    self.pos_delay_active = True
                    self.vector = (AI_Calculations.direction_turner((0, self.pos[1]),(0, target_pos[1])))
                    self.pos_countdown = AI_Calculations.get_time(self.pos[1], target_pos[1], self.speed)
            else: self.spawn_2()

    def spawn_2(self):
        
        if self.spawn_state == 1:
            self.spawn_state = 2
            self.instant_target_point = (13.5, 17)
            target_pos = ((self.instant_target_point[0]*TILE_SIZE),(self.instant_target_point[1]*TILE_SIZE))
            if target_pos [0] != self.pos[0]:
                self.pos_delay_active = True
                self.vector = (AI_Calculations.direction_turner((self.pos[0], 0),(target_pos[0], 0)))
                self.pos_countdown = AI_Calculations.get_time(self.pos[0], target_pos[0], self.speed)
            else: self.spawn_3()
     

    def spawn_3(self):

        if self.spawn_state == 2:
            self.spawn_state = 3
            self.instant_target_point = (13.5, 14)
            target_pos = ((self.instant_target_point[0]*TILE_SIZE),(self.instant_target_point[1]*TILE_SIZE))
            self.pos_delay_active = True
            self.vector = (AI_Calculations.direction_turner((0, self.pos[1]),(0, target_pos[1])))
            self.pos_countdown = AI_Calculations.get_time(self.pos[1], target_pos[1], self.speed)


    def spawn_countdown(self):
        if self.AI_mode == "Spawn":
            self.spawn_delay_time -= 1
            if self.spawn_delay_time <= 0:
                 self.spawn_1()


    def animate(self):
        
        self.animation_countdown += 1
        if self.animation_countdown >= 65:
            if self.animation_state == 1:
                self.animation_state = 2
            elif self.animation_state == 2:
                 self.animation_state = 1
            self.animation_countdown = 0
            self.update_image()

    def drawer(self):
        self.display.blit(self.image, (self.pos))
        #pygame.draw.rect(self.display, (0,255,0), self.hitbox_rect)

    def tick(self):

        self.spawn_countdown()
        self.animate()
        self.movement_countdown()
    
    def update(self):
        if self.AI_mode == "Chase":
            self.aquire_target()
        if self.coordinates == self.instant_target_point:
                self.pos_delay_active = True
        self.tick()
        self.move(self.speed)
        self.drawer()
        #if self.identifier == "Pinky":


        

