from csv import reader
from os import walk
import pygame
def csv_layout(path):
    map = []
    with open(path) as level_map:
        layout = reader (level_map, delimiter = ',')
        for row in layout:
            map.append(list(row))
        return map

def import_folder(path):
    surface_list = []
    for __,__,img_files  in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
        return surface_list



