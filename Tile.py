from Set_Up import *

class Tile():
    def __init__(self, pos):

        self.display = pygame.display.get_surface()
        self.coordinates = (pos)
        self.sprite = None
        self.wall = False
        self.draw = False
        self.rgb = (255, 255 ,255)
        self.rect = pygame.Rect(pos[0]*TILE_SIZE, pos[1]*TILE_SIZE, TILE_SIZE/2, TILE_SIZE/2)
        
    #for testing
    def drawer(self):

        pygame.draw.rect(self.display, self.rgb, self.rect)





