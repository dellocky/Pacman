# -*- coding: utf-8 -*-awa
"""aaaaaaaaaaa
Created on Wed Aug  9 15:24:56 2023

@author: footb
"""
import pygame, sys
from Set_Up import *
from Level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock=pygame.time.Clock()
        
        self.level= Level()
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    
    Pacman = Game()
    Pacman.run()