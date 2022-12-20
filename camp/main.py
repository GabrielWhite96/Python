import pygame
from pygame.locals import *
from sys import exit

pygame.init()

pygame.display.set_caption('Game')

width_screen = 1280
heigh_screen = 720

screen = pygame.display.set_mode((width_screen, heigh_screen))

auxHeigh = True
auxY = 0

movex = 600
movey = 300

clock = pygame.time.Clock()

while True:
  screen.fill((0, 0, 0))
  clock.tick(60)

  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      exit()
    # if event.type == KEYDOWN:
    #   if event.key == K_w:
    #     movey = movey - 10
    #   if event.key == K_a:
    #     movex = movex - 10
    #   if event.key == K_s:
    #     movey = movey + 10
    #   if event.key == K_d:
    #     movex = movex + 10
    
  if pygame.key.get_pressed()[K_w]:
    movey = movey - 5
  if pygame.key.get_pressed()[K_a]:
    movex = movex - 5
  if pygame.key.get_pressed()[K_s]:
    movey = movey + 5
  if pygame.key.get_pressed()[K_d]:
    movex = movex + 5
        
        

  pygame.draw.rect(screen, (255, 100, 0), (200, 300, 50, 50))
  pygame.draw.circle(screen, (0, 100, 255), (300, 325), 25)
  pygame.draw.line(screen, (50, 255, 50), (350, 200), (350, 450), 5)
  pygame.draw.line(screen, (50, 255, 50), (400, 300), (450, 300), 2)
  pygame.draw.line(screen, (10, 255, 50), (450, 300), (450, 350), 2)
  pygame.draw.line(screen, (50, 255, 50), (450, 350), (400, 350), 2)
  pygame.draw.line(screen, (50, 255, 50), (400, 350), (400, 300), 2)

  pygame.draw.rect(screen, (255, 0, 0), (500, auxY, 50, 50))
  if auxHeigh:
    if auxY <= heigh_screen-50:
      auxY = auxY + 3
    else:
      auxHeigh = False
  else:
    if auxY >= 0:
      auxY = auxY - 3
    else:
      auxHeigh = True
      
  pygame.draw.rect(screen, (0, 255, 150), (movex, movey, 50, 50))
  
  
  
  

  pygame.display.update()
