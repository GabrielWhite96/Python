import sys

import pygame
# from editor import Editor
from pygame.image import load
from settings import *


class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Flappy Bird')
        self.fps = pygame.time.Clock()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        
    def run(self):
        while True:
            self.fps.tick(60)
                    
            
            pygame.display.update()
            
if __name__ == '__main__':
    main = Main()
    main.run()