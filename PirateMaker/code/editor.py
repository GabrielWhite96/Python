import pygame, sys
from settings import *
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos
from pygame.math import Vector2 as vector

class Editor:
    def __init__(self):
        # main setup
        self.display_surface = pygame.display.get_surface()
        
        # navigation
        self.origin = vector(0, 0)
        self.pan_active = False
        self.pan_offset = vector()
    
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            self.pan_input(event)
    
    def pan_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[1]:
            self.pan_active = True
            self.pan_offset =  vector(mouse_pos()) - self.origin
        if not mouse_buttons()[1]:
            self.pan_active = False
            
        if event.type == pygame.MOUSEWHEEL:
            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                self.origin.y -= event.y*10
            else:
                self.origin.x -= event.y*10
            
        # panning update
        if self.pan_active:
            self.origin = vector(mouse_pos()) - self.pan_offset
    
    def draw_tile_lines(self):
        cols = WINDOW_WIDTH // TILE_SIZE
        rows = WINDOW_HEIGHT // TILE_SIZE
        
        for col in range(cols):
            x = self.origin.x + col * TILE_SIZE
            pygame.draw.line(self.display_surface, LINE_COLOR, (x, 0), (x, WINDOW_HEIGHT))
    
    def run(self, dt):
        self.event_loop()
        
        # drawing
        self.display_surface.fill('white')
        self.draw_tile_lines()
        
        pygame.draw.circle(self.display_surface, 'blue', self.origin, 20)