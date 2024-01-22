# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 18:56:35 2023

@author: footb
"""


from Set_Up import *
    
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, object_sprites):
        super().__init__(groups)
        self.pos = pos
        self.coordinates = (round(pos[0] / TILE_SIZE, 0), round(pos[1] / TILE_SIZE, 0))
        self.image = pygame.image.load('Assets/Pacman Model/Player Left.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.image = pygame.transform.smoothscale(self.image, (20, 20))

        self.hitbox = self.rect.inflate(-7.5, -7.5)
        self.hitbox.x-=1.5
        self.hitbox.y-=1.5
        self.last_direction='left'

        self.rect = self.hitbox

        self.direction = (0, 0)
        self.speed = .675

        self.obstacle_sprites = obstacle_sprites
        self.object_sprites = object_sprites

        self.animation_time=0

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction = (0, -1)
            self.image = pygame.image.load('Assets/Pacman Model/Player Up.png').convert_alpha()
            self.image = pygame.transform.smoothscale(self.image, (20, 20))
            self.animation_time += 1
            self.last_direction = 'up'
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction = (0, 1)
            self.image = pygame.image.load('Assets/Pacman Model/Player Down.png').convert_alpha()
            self.image = pygame.transform.smoothscale(self.image, (20, 20))
            self.animation_time += 1
            self.last_direction = 'down'
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction = (1, 0)
            self.image = pygame.image.load('Assets/Pacman Model/Player Right.png').convert_alpha()
            self.image = pygame.transform.smoothscale(self.image, (20, 20))
            self.animation_time += 1
            self.last_direction = 'right'
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction = (-1, 0)
            self.image = pygame.image.load('Assets/Pacman Model/Player Left.png').convert_alpha()
            self.image = pygame.transform.smoothscale(self.image, (20, 20))
            self.animation_time += 1
            self.last_direction = 'left'
        else:
            self.direction = (0, 0)
            self.animation_time=0
            if self.last_direction == 'up':
                self.image = pygame.image.load('Assets/Pacman Model/Player Up.png').convert_alpha()
                self.image = pygame.transform.smoothscale(self.image, (20, 20))
            if self.last_direction == 'down':
                self.image = pygame.image.load('Assets/Pacman Model/Player Down.png').convert_alpha()
                self.image = pygame.transform.smoothscale(self.image, (20, 20))
            if self.last_direction == 'right':
                self.image = pygame.image.load('Assets/Pacman Model/Player Right.png').convert_alpha()
                self.image = pygame.transform.smoothscale(self.image, (20, 20))
            if self.last_direction == 'left':
                self.image = pygame.image.load('Assets/Pacman Model/Player Left.png').convert_alpha()
                self.image = pygame.transform.smoothscale(self.image, (20, 20))


    def update_coordinates(self):
        self.coordinates = (round(self.pos[0] / TILE_SIZE, 0), round(self.pos[1] / TILE_SIZE, 0))

    def move(self, speed):

        self.pos = (self.pos[0]+self.direction[0]*speed, self.pos[1]+self.direction[1]*speed)
        self.rect.topleft = (self.pos)

        if self.rect.x < -16:

            self.pos =(456, self.pos[1])


        if self.rect.x > 456:

            self.pos=(-16, self.pos[1])

        self.update_coordinates()

    def animate(self):

        current_image = self.image
        if self.animation_time<10:
            self.image = current_image

        elif self.animation_time<20:
            full_image = pygame.image.load('Assets/Pacman Model/Player Full.png').convert_alpha()
            self.image = full_image
            self.image = pygame.transform.smoothscale(self.image, (20, 20))

        if self.animation_time>=20:
            self.image=current_image
            self.animation_time=0



    def wall_collision(self, direction):
        if direction[0] !=0:
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction[0] < 0:
                         self.rect.left = sprite.hitbox.right
                         self.pos = (self.rect.topleft)
                         self.direction = (0, 0)

                    if self.direction[0] > 0:
                         self.rect.right = sprite.hitbox.left
                         self.pos = (self.rect.topleft)
                         self.direction = (0, 0)

        if direction[1] != 0:
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.rect):
                    if self.direction[1] < 0:
                        self.rect.top = sprite.hitbox.bottom
                        self.pos = (self.rect.topleft)
                        self.direction = (0, 0)

                    if self.direction[1] > 0:
                        self.rect.bottom = sprite.hitbox.top
                        self.pos = (self.rect.topleft)
                        self.direction = (0, 0)


    def object_collision(self):
        for sprite in self.object_sprites:
            if sprite.rect.colliderect(self.rect):
                sprite.kill()


    def update(self):
        self.input()
        self.move(self.speed)
        self.object_collision()
        self.wall_collision(self.direction)
        self.animate()

        
