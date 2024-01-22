def neighbor_tile_calculator(coordinates):
    neighbors = [(coordinates[0] + 1, coordinates[1]),
                 (coordinates[0] - 1, coordinates[1]),
                 (coordinates[0], coordinates[1] + 1),
                 (coordinates[0], coordinates[1] - 1)]
    return neighbors

def remove_opposite_direction(neighbors, direction):

    if direction == (-1, 0):
        del(neighbors[0])
        return neighbors

    if direction == (1, 0):
        del(neighbors[1])
        return neighbors

    if direction == (0, -1):
        del(neighbors[2])
        return neighbors

    if direction == (0, 1):
        del(neighbors[3])
        return neighbors

def distance_calculator(potential_tiles, player_coordinates):

    player_distance=[]
    for tile in potential_tiles:
        player_distance.append(abs(tile[0]-player_coordinates[0])+abs(tile[1]-player_coordinates[1]))
    selected_coordinate=potential_tiles[player_distance.index(min(player_distance))]
    return selected_coordinate

def direction_turner(current_coordinate, selected_coordinate):

    if selected_coordinate[0] > current_coordinate [0]:
        direction = (1, 0)
        return direction

    elif selected_coordinate[0] < current_coordinate [0]:
        direction = (-1, 0)
        return direction

    elif selected_coordinate[1] > current_coordinate[1]:
        direction = (0, 1)
        return direction

    elif selected_coordinate[1] < current_coordinate[1]:
        direction = (0, -1)
        return direction




