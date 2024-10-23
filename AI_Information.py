from Set_Up import *


def get_values(name):

    if name == 'Blinky':
        pos = (TILE_SIZE*13.5, TILE_SIZE*14)
        instant_target_point = (12,14)
        
        vector = (-1, 0)
        direction = "Left"
        
        AI_mode = "Chase"
        spawn_state = 0
        spawn_delay_time = 0
        
    elif name == 'Pinky':
        pos = (TILE_SIZE*13.5, TILE_SIZE*17)
        instant_target_point = (14, 16)
        
        vector = (0, -1)
        direction = "Up"
        
        AI_mode = "Spawn"
        spawn_state = 0
        spawn_delay_time = FPS * 8
        
    elif name == 'Inky':
        pos = (TILE_SIZE*11.5, TILE_SIZE*17)
        instant_target_point = (12, 18)
        
        vector = (0, 1)
        direction = "Down"
        
        AI_mode = "Spawn"
        spawn_state = 0
        spawn_delay_time = FPS * 16
        
    elif name == 'Clyde':
        pos = (TILE_SIZE*15.5, TILE_SIZE*17)
        instant_target_point = (16, 18)
        
        vector = (0, 1)
        direction = "Down"
        
        AI_mode = "Spawn"
        spawn_state = 0
        spawn_delay_time = FPS * 24

    return(pos, instant_target_point, vector, direction, AI_mode, spawn_state, spawn_delay_time)

def get_target_point_chase(name, player):

    if name == 'Blinky':
        target_point = player.coordinates

    if name == 'Pinky':
        target_point = ((player.coordinates[0]+player.vector[0]*2), (player.coordinates[1]+player.vector[1]*2))

    if name == 'Inky':
        target_point = ((player.coordinates[0]-player.vector[0]*2), (player.coordinates[1]-player.vector[1]*2))
        
    if name == 'Clyde':
        target_point = ((round(player.coordinates[0]-player.vector[0]*6)), (round(player.coordinates[1]-player.vector[1]*6)))
    
    return target_point

def get_target_point_flee(player):

    mid_coordinate = (WIDTH/2, HEIGHT/2)
    distanse = (mid_coordinate[0]-player.coordinates[0], mid_coordinate[1]-player.coordinates[1])
    return (mid_coordinate[0]+distanse[0], mid_coordinate[1]+distanse[1])

def get_target_point(name, coordinate, AI_mode, player):

    if AI_mode == "Chase":
        return get_target_point_chase(name, player) 
    
    if AI_mode == "Flee":
        return get_target_point_flee(player) 


def get_direction(vector):
    
    if vector == (1, 0):
        direction = "Right"
        
    elif vector == (-1, 0):
        direction = "Left"

    elif vector == (0, 1):
        direction = "Down"

    elif vector == (0, -1):
        direction = "Up"

    return direction

def get_behavior(AI_mode, mode_state):

    if AI_mode == "Chase":
        return 'navigate', AI_mode, mode_state
    elif AI_mode == "Spawn" and mode_state == 0:
        return 'direction_flip', AI_mode, mode_state
    elif AI_mode == "Spawn" and mode_state == 1:
        return 'spawn_2', AI_mode, mode_state
    elif(AI_mode == "Spawn" or AI_mode == "Eaten") and mode_state == 2:
        return 'exit_spawn', AI_mode, mode_state
    elif (AI_mode == "Spawn" or AI_mode == "Eaten") and mode_state == 3:
        AI_mode = "Chase"
        mode_state = 0
        return 'navigate', AI_mode, mode_state
    elif AI_mode == "Flee":
        return 'navigate', AI_mode, mode_state
    elif AI_mode == "Eaten" and mode_state == 0:
        return 'eaten_0', AI_mode, mode_state
    elif AI_mode == "Eaten" and mode_state == 1:
        return 'eaten_2', AI_mode, mode_state

        