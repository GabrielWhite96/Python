import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

pygame.display.set_caption('Game')
clock = pygame.time.Clock()

width_screen = 400
heigh_screen = 800
falling_speed = 10
scenery_speed = 5
gravity = 1
screen = pygame.display.set_mode((width_screen, heigh_screen))

bird_sprites = []

sprite_up = pygame.image.load('assets/sprites/davi.png').convert_alpha()
sprite_up = pygame.transform.scale(sprite_up, (80, 80))
sprite_mid = pygame.image.load('assets/sprites/davi.png').convert_alpha()
sprite_mid = pygame.transform.scale(sprite_mid, (80, 80))
sprite_down = pygame.image.load('assets/sprites/davi.png').convert_alpha()
sprite_down = pygame.transform.scale(sprite_down, (80, 80))

class Bird(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.images = [pygame.image.load('assets/sprites/pink1.png').convert_alpha(),
                       pygame.image.load('assets/sprites/pink2.png').convert_alpha(),
                       pygame.image.load('assets/sprites/pink3.png').convert_alpha()]
        
        self.current_image = 0
        
        self.speed = 0
        
        self.image = pygame.image.load('assets/sprites/pink1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect[0] = width_screen/2
        self.rect[1] = heigh_screen/2
        
    def update(self):
        self.current_image = (self.current_image + 1)%3
        self.image = self.images[self.current_image]
        
        self.speed += gravity 
        
        self.rect[1] += self.speed
        
    def bump(self):
        self.speed = -falling_speed
        
class Ground(pygame.sprite.Sprite):
    
    def __init__(self, width, heigh, xpos):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('assets/sprites/base.png')
        self.image = pygame.transform.scale(self.image, (width, heigh))
        
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = heigh_screen - heigh
        
    def update(self):
        self.rect[0] -= scenery_speed
        
    
        

background_img = pygame.image.load('assets/sprites/background-day.png')
background_img = pygame.transform.scale(background_img, (width_screen, heigh_screen))

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(2 * width_screen, 100, 2 * width_screen *i)
    ground_group.add(ground)
    

while True:
    clock.tick(30)    
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == K_SPACE:
                bird.bump()
                
    screen.blit(background_img, (0, 0))
    
    bird_group.update()
    bird_group.draw(screen)
     
    ground_group.update()
    ground_group.draw(screen)
    
    pygame.display.update()