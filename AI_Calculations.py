from Set_Up import *


def neighbor_tile_calculator(coordinates):
    neighbors = [(coordinates[0] + 1, coordinates[1], True),
                 (coordinates[0] - 1, coordinates[1], True),
                 (coordinates[0], coordinates[1] + 1, True),
                 (coordinates[0], coordinates[1] - 1, True)]

    return neighbors

def remove_opposite_direction(neighbors, vector):

    if vector == (-1, 0):
        del(neighbors[0])
        return neighbors

    if vector == (1, 0):
        del(neighbors[1])
        return neighbors

    if vector == (0, -1):
        del(neighbors[2])
        return neighbors

    if vector == (0, 1):
        del(neighbors[3])
        return neighbors

def distance_calculator(potential_tiles, target_coordinates):

    player_distance=[]

    for tile in potential_tiles:
        if tile[2] == True:
            player_distance.append(abs(tile[0] - target_coordinates[0]) + abs(tile[1] - target_coordinates[1]))
    selected_coordinate=potential_tiles[player_distance.index(min(player_distance))]
    return selected_coordinate

def direction_turner(current_coordinate, selected_coordinate):

    if selected_coordinate[0] > current_coordinate [0]:
        vector = (1, 0)
        return vector

    elif selected_coordinate[0] < current_coordinate [0]:
        vector = (-1, 0)
        return vector

    elif selected_coordinate[1] > current_coordinate[1]:
        vector = (0, 1)
        return vector

    elif selected_coordinate[1] < current_coordinate[1]:
        vector = (0, -1)
        return vector
    
    
def turn_around(vector):
    
    if vector == (1, 0):
        return (-1, 0)

    elif vector == (-1, 0):
        return (1, 0)
    
    elif vector == (0, 1):
        return (0, -1)
    
    elif vector == (0, -1):
        return (0, 1)
    
def get_time(pos1, pos2, speed):

    distanse = abs(pos1 - pos2)
    time = distanse/speed
    return round(time)

def validate_neighbors(coordinates_list, tiles):

    valid_neighbors = []
    for coordinates in coordinates_list:
        append = True
        if coordinates[0] >= WIDTH or coordinates[0] < 0 or coordinates[1] >= HEIGHT or coordinates[1] < 0:
            continue
        for tile in tiles:
            if tile.coordinates == coordinates[0:2] and tile.pathed == False:
                if tile.sprite:
                    for group in tile.sprite.groups:
                        if group.name == 'wall_sprites':
                            append = False
            
                if append == True:
                    valid_neighbors.append(coordinates[0:2])
                    tile.pathed = True

        
    return valid_neighbors
                           

def cascade(path_list, tiles) -> list:

    all_list = list()
    all_list.clear()
    for path in path_list:
        starting_point = path[-1]
        neighbor_list = validate_neighbors(neighbor_tile_calculator(starting_point), tiles)
        for tile in neighbor_list:
            current_list = (path[:])
            current_list.append(tile)
            all_list.append(current_list)
    return all_list

