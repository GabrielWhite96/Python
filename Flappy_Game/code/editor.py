import pygame
from settings import *

class Editor:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        
    def set_background(self, background):
        self.display_surface.blit(background,(0,0))
        