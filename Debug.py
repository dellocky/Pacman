# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 00:48:16 2023

@author: footb
"""

import pygame

pygame.init()
font=pygame.font.Font(None, 25)

def debug(info, x=10 ,y=10):
    display_surface=pygame.display.get_surface()
    debug_surf=font.render(str(info), True, "red")
    debug_rect=debug_surf.get_rect(topleft=(x,y))
    display_surface.blit(debug_surf,debug_rect)

def highlight_hitbox(highlight_box, image, color):

    highlight = pygame.Surface(highlight_box.size)
    if color == "yellow":
        highlight.fill((255, 255, 0))
    if color == "green":
        highlight.fill((0, 255, 0))
    highlight.set_alpha(128)
    image.blit(highlight, (4, 4))
