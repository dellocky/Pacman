import pygame
import CSV
import AI_Calculations
import AI_Information
import C_Interface
import Debug
import Sprite
from Set_Up import *


class Enemy(Sprite.Sprite):
    def __init__(self, name, groups, player, obstacle_sprites, tiles, flag_map):
     
        self.pos, self.instant_target_point, self.vector, self.direction, self.AI_mode, self.mode_state, self.spawn_delay_time = AI_Information.get_values(name)
        super().__init__(name, self.pos, (TILE_SIZE/2), groups)
    
        self.player = player
        self.player_point = self.player.coordinates
        self.target_point = None
        
        self.path = []
        self.path_index = 0

        self.hitbox_rect = pygame.Rect(0,0,TILE_SIZE/2,TILE_SIZE/2)
        self.hitbox_rect.center = (self.pos[0]+(TILE_SIZE/2),self.pos[1]+(TILE_SIZE/2))
    
        self.base_images = CSV.import_folder_dict(f'Assets/Ghosts/{self.name}', (TILE_SIZE*1.25, TILE_SIZE*1.25))
        self.eaten_images = CSV.import_folder_dict('Assets/Ghost States/Eaten', (TILE_SIZE*1.25, TILE_SIZE*1.25))
        self.highlighted_images = CSV.import_folder_dict('Assets/Ghost States/Highlighted', (TILE_SIZE*1.25, TILE_SIZE*1.25))
      

        self.potential_directions = []

        self.pos_time = round((TILE_SIZE/2)/self.speed)
        self.pos_countdown = 0
        self.pos_delay_active = False

        self.animation_state = 1
        self.animation_countdown = 0

        self.update_image_default()
        self.obstacle_sprites = obstacle_sprites
        self.tiles = tiles
        self.flag_map = flag_map
    
    def update_image_default(self):
            self.image = self.base_images[f"{self.name} Eyes {self.direction} {self.animation_state}"]
    
    def update_image_highlight_blue(self): 
            self.image = self.highlighted_images[f"Highlighted Blue {self.animation_state}"]
    
    def update_image_highlight_white(self):
            self.image = self.highlighted_images[f"Highlighted White {self.animation_state}"]

    def update_image_eaten(self):
            self.image = self.eaten_images[f"Eyes {self.direction}"]

    
    def act(self):
        function, self.AI_mode, self.mode_state = AI_Information.get_behavior(self.AI_mode, self.mode_state)
        getattr(self, function)()
    
    def aquire_target(self):

        self.target_point = AI_Information.get_target_point(self.name, self.coordinates, self.AI_mode, self.player)
    
    def turn(self, vector):
        self.vector = vector
        self.direction = AI_Information.get_direction(vector)
        self.update_image()


    def direction_flip(self):
        self.turn(AI_Calculations.turn_around(self.vector))
        self.instant_target_point = (self.coordinates[0]+(self.vector[0]*2), self.coordinates[1]+(self.vector[1]*2))

    def direction_change(self):
        self.turn(AI_Calculations.direction_turner(self.coordinates, self.instant_target_point))

    #flee triggers
    def initiate_flee(self):
        
        if self.AI_mode == "Chase" or self.AI_mode == "Scatter":
            self.AI_mode = "Flee"
            self.speed *= .75

    def end_flee(self):
         if self.AI_mode == "Flee":
             self.AI_mode = "Chase"
             self.speed *= 4.0/3.0

    #eaten triggers
    def initiate_eaten(self):
        if self.AI_mode == "Flee":
            self.AI_mode = "Eaten"
            self.mode_state = 0
            self.speed *= 4.0/3.0
            self.create_path()

            

    def navigate(self):
        self.aquire_target()
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
    
    #pathfinding algorithim, ensures ghosts find there way back to ghost house using fastest possible path
    @Debug.get_time
    def create_path(self):

        target_coordinates = [(13, 14),(14, 14)]
        input_coordinates = (int(self.player.coordinates[0]),int(self.player.coordinates[1]))
        C_Interface.c_path_finder(self.flag_map, input_coordinates, target_coordinates)
        #C_Interface.c_maze_visualizer(self.flag_map)
        #C_Interface.c_debug(self.flag_map, input_coordinates, target_coordinates)
    
    #spawn behavior
    def spawn_1(self):
        if self.mode_state != 0:
            return
        
        self.mode_state = 1
        if self.coordinates != 14:
            self.instant_target_point = (self.coordinates[0], 17)
            target_pos = ((self.instant_target_point[0]*TILE_SIZE),(self.instant_target_point[1]*TILE_SIZE))
            if self.pos == target_pos:
                self.spawn_2()
            else:
                self.pos_delay_active = True
                self.turn(AI_Calculations.direction_turner((0, self.pos[1]),(0, target_pos[1])))
                self.pos_countdown = AI_Calculations.get_time(self.pos[1], target_pos[1], self.speed)
        else: self.spawn_2()

    def spawn_2(self):
        
        if self.mode_state != 1:
            return
        
        self.mode_state = 2
        self.instant_target_point = (13.5, 17)
        target_pos = ((self.instant_target_point[0]*TILE_SIZE),(self.instant_target_point[1]*TILE_SIZE))
        if target_pos [0] != self.pos[0]:
            self.pos_delay_active = True
            self.turn((AI_Calculations.direction_turner((self.pos[0], 0),(target_pos[0], 0))))
            self.pos_countdown = AI_Calculations.get_time(self.pos[0], target_pos[0], self.speed)
        else: self.exit_spawn()
    
    def exit_spawn(self):
        
        self.AI_mode = "Spawn"
        if self.mode_state != 2:
            return
        
        self.mode_state = 3
        self.instant_target_point = (13.5, 14)
        target_pos = ((self.instant_target_point[0]*TILE_SIZE),(self.instant_target_point[1]*TILE_SIZE))
        self.pos_delay_active = True
        self.turn(AI_Calculations.direction_turner((0, self.pos[1]),(0, target_pos[1])))
        self.pos_countdown = AI_Calculations.get_time(self.pos[1], target_pos[1], self.speed)


    def eaten_0(self):


        if self.path_index < len(self.path)-1:
            
            self.pos_delay_active = True
            target_point = self.path[self.path_index+1]
            target_pos = ((target_point[0]*TILE_SIZE),((target_point[1]*TILE_SIZE)))
            self.turn(AI_Calculations.direction_turner(self.path[self.path_index], self.path[self.path_index+1]))
            
            if self.path[self.path_index][0] != self.path[self.path_index+1][0]:
                self.pos_countdown = AI_Calculations.get_time(self.pos[0], target_pos[0], self.speed)

            else:
                self.pos_countdown = AI_Calculations.get_time(self.pos[1], target_pos[1], self.speed)
                
            if self.coordinates[0] != self.path[self.path_index+1][0] and self.coordinates[1] != self.path[self.path_index+1][1]:
                pass
            
            self.path_index += 1

        else:
            self.eaten_1()

    def eaten_1(self):
        
        self.mode_state = 1
        self.instant_target_point = (13.5, 14)
        target_pos = ((self.instant_target_point[0]*TILE_SIZE),(self.instant_target_point[1]*TILE_SIZE))
        self.pos_delay_active = True
        self.turn(AI_Calculations.direction_turner((self.pos[0], 0),(target_pos[0], 0)))
        self.pos_countdown = AI_Calculations.get_time(self.pos[0], target_pos[0], self.speed)

    def eaten_2(self):
        
        self.mode_state = 2
        self.instant_target_point = (13.5, 17)
        target_pos = ((self.instant_target_point[0]*TILE_SIZE),(self.instant_target_point[1]*TILE_SIZE))
        self.pos_delay_active = True
        self.turn(AI_Calculations.direction_turner((0, self.pos[1]),(0, target_pos[1])))
        self.pos_countdown = AI_Calculations.get_time(self.pos[1], target_pos[1], self.speed)


    #animation behavior
    def animate_movement(self):
        if self.animation_countdown >= 65:
            if self.animation_state == 1:
                self.animation_state = 2
            elif self.animation_state == 2:
                    self.animation_state = 1
            self.animation_countdown = 0
    
    def animate_flee(self):
        
        if self.player.empowered_time > FPS * 1.5:
            self.update_image_highlight_blue()
        if self.player.empowered_time <= FPS * 1.5:
            if self.player.empowered_time % 30 >= 15:
                self.update_image_highlight_white()
            else:
                self.update_image_highlight_blue()
        

    def update_image(self):
        
        self.animate_movement()
        if self.AI_mode == "Flee":
            self.animate_flee()
        elif self.AI_mode == "Eaten":
            self.update_image_eaten()
        else: self.update_image_default()


    def movement_tick(self):
    
        if self.coordinates == self.instant_target_point:
                self.pos_delay_active = True
        if self.pos_delay_active is False:
            return
        self.pos_countdown -=1
        if self.pos_countdown <= 0:
            self.pos_delay_active = False
            self.pos_countdown = self.pos_time
            self.act()
    
    def spawn_tick(self):
        if self.AI_mode == "Spawn":
            self.spawn_delay_time -= 1
            if self.spawn_delay_time <= 0:
                 self.spawn_1()
    
    def animate_tick(self):
        self.animation_countdown += 1
        self.update_image()

    def tick(self):

        self.movement_tick()
        self.spawn_tick()
        self.animate_tick()
       

    def update(self):

        self.aquire_target()
        self.tick()
        self.move(self.speed)
        self.draw()
        #if self.name == "Blinky":
            #Debug.debug((self.AI_mode, self.mode_state))
        


        

