import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

pygame.display.set_caption('Game')
clock = pygame.time.Clock()

width_screen = 400
height_screen = 800
falling_speed = 10
scenery_speed = 5
gravity = 1
ground_width = 2 * width_screen
ground_height = 100
pipe_width = 120
pipe_height = 500

screen = pygame.display.set_mode((width_screen, height_screen))

background_img = pygame.image.load('assets/sprites/background-day.png')
background_img = pygame.transform.scale(background_img, (width_screen, height_screen))

# sprite_up = pygame.image.load('assets/sprites/davi.png').convert_alpha()
# sprite_up = pygame.transform.scale(sprite_up, (80, 80))
# sprite_mid = pygame.image.load('assets/sprites/davi.png').convert_alpha()
# sprite_mid = pygame.transform.scale(sprite_mid, (80, 80))
# sprite_down = pygame.image.load('assets/sprites/davi.png').convert_alpha()
# sprite_down = pygame.transform.scale(sprite_down, (80, 80))

class Bird(pygame.sprite.Sprite):
    
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    
    self.images = [pygame.image.load('assets/sprites/pink1.png').convert_alpha(),
                   pygame.image.load('assets/sprites/pink2.png').convert_alpha(),
                   pygame.image.load('assets/sprites/pink3.png').convert_alpha()]
    
    self.image = pygame.image.load('assets/sprites/pink1.png').convert_alpha()
    
    self.current_image = 0
    
    self.mask = pygame.mask.from_surface(self.image)
    
    self.speed = 0
    
    self.rect = self.image.get_rect()
    self.rect[0] = width_screen/2
    self.rect[1] = height_screen/2
      
  def update(self):
    self.current_image = (self.current_image + 1)%3
    self.image = self.images[self.current_image]
    
    self.speed += gravity 
    
    self.rect[1] += self.speed
      
  def bump(self):
    self.speed = -falling_speed
    
    
class Pipe(pygame.sprite.Sprite):
  
  def __init__(self, inverted, xpos, ysize):
    pygame.sprite.Sprite.__init__(self)
    
    self.image = pygame.image.load('assets/sprites/pipe-black.png').convert_alpha()
    self.image = pygame.transform.scale(self.image, (pipe_width, pipe_height))
    
    self.rect = self.image.get_rect()
    self.rect[0] = xpos
    
    if inverted:
      self.image = pygame.transform.flip(self.image, False, True)
      self.rect[1] = -(self.rect[3] - ysize)
    else:
      self.rect[1] = height_screen - ysize
    
    self.mask = pygame.mask.from_surface(self.image)
    
  def update(self):
    self.rect[0] -= scenery_speed
        
        
class Ground(pygame.sprite.Sprite):
    
  def __init__(self, xpos):
    pygame.sprite.Sprite.__init__(self)
    
    self.image = pygame.image.load('assets/sprites/base.png').convert_alpha()
    self.image = pygame.transform.scale(self.image, (ground_width, ground_height))
    
    self.mask = pygame.mask.from_surface(self.image)
    
    self.rect = self.image.get_rect()
    self.rect[0] = xpos
    self.rect[1] = height_screen - ground_height
        
    def update(self):
      self.rect[0] -= scenery_speed
        
        
def is_off_screen(sprite):
  return sprite.rect[0] < -(sprite.rect[2])
        

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

pipe_group = pygame.sprite.Group()


ground_group = pygame.sprite.Group()
for i in range(2):
  ground = Ground(ground_width *i)
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
  
  if is_off_screen(ground_group.sprites()[0]):
    ground_group.remove(ground_group.sprites()[0])
    new_ground = Ground(ground_width-20)
    ground_group.add(new_ground)
      
  bird_group.update()
  bird_group.draw(screen)
    
  ground_group.update()
  ground_group.draw(screen)
  

  pygame.display.update()
  
  if pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask):
    break