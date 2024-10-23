from Set_Up import *
import pygame
import Tile

class Sprite():
    def __init__(self, name, coordinates, hitbox_rect_size, groups = []) -> None:      
    
        self.name = name
        self.groups = groups

        self.pos = coordinates
        self.coordinates = (round(self.pos[0] / TILE_SIZE, 0), round(self.pos[1] / TILE_SIZE, 0))

        self.hitbox_rect = pygame.Rect(0,0, hitbox_rect_size, hitbox_rect_size)
        self.hitbox_rect.center = (self.pos[0]+(TILE_SIZE/2),self.pos[1]+(TILE_SIZE/2))
        self.speed = .575
        self.display = pygame.display.get_surface()

        if groups != False:
            for I in groups:
                I.append(self)
    
    def update_coordinates(self):
        self.coordinates = (round(self.pos[0] / TILE_SIZE, 0), round(self.pos[1] / TILE_SIZE, 0))

    def move(self, speed):
        self.pos = (self.pos[0]+self.vector[0]*speed, self.pos[1]+self.vector[1]*speed)
        self.hitbox_rect.center = (self.pos[0]+(TILE_SIZE/2),self.pos[1]+(TILE_SIZE/2))

        if self.hitbox_rect.x < -8:

            self.pos =(442, self.pos[1])


        elif self.hitbox_rect.x > 448:

            self.pos=(-6, self.pos[1])

        self.update_coordinates()
    
    def draw(self):
        self.display.blit(self.image, (self.pos))
        #pygame.draw.rect(self.display, (0,255,0), self.hitbox_rect)