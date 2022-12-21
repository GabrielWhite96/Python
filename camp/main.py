import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

pygame.display.set_caption('Game')


back_music = pygame.mixer.music.load('backMusic.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

coli_sound = pygame.mixer.Sound('smb3_coin.wav')
coli_sound.set_volume(0.1)

background_image = pygame.image.load('2.png')

width_screen = 1280
heigh_screen = 720

screen = pygame.display.set_mode((width_screen, heigh_screen))

# auxHeigh = True
# auxY = 0

speed = 20
x_control = speed
y_control = 0
x_snake = int(width_screen/2)
y_snake = int(heigh_screen/2)
x_apple = randint(50, 1230)
y_apple = randint(50, 670)

font = pygame.font.SysFont('arial', 40, True, False)
points = 0

clock = pygame.time.Clock()

snake_length = 5

died = False

snake_list = []
def add_snake(snake_list):
  for XandY in snake_list:
    pygame.draw.rect(screen, (0, 200, 50), (XandY[0],XandY[1] , 20, 20))

def restart_game():
  global points, snake_length, x_snake, y_snake, x_apple, y_apple, head_list, snake_list, died
  points = 0
  snake_length = 5
  x_snake = int(width_screen/2)
  y_snake = int(heigh_screen/2)
  x_apple = randint(50, 1230)
  y_apple = randint(50, 670)
  head_list = []
  snake_list = []
  died = False

while True:
  screen.fill((0, 0, 0))
  clock.tick(10)
  
  msg_points = f'Pontos: {points}'
  formated_text = font.render(msg_points, True, (255, 255, 255))
  
  screen.blit(background_image, (0, 0))

  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      exit()
      
    if event.type == KEYDOWN:
      if event.key == K_ESCAPE:
        pygame.quit()
        exit()
      if event.key == K_w:
        if y_control == speed:
          pass
        else:
          x_control = 0
          y_control = -speed
      if event.key == K_a:
        if x_control == speed:
          pass
        else:
          x_control = -speed
          y_control = 0
      if event.key == K_s:
        if y_control == -speed:
          pass
        else:
          x_control = 0
          y_control = speed
      if event.key == K_d:
        if x_control == -speed:
          pass
        else:
          x_control = speed
          y_control = 0
    
  x_snake = x_snake + x_control
  y_snake = y_snake + y_control
  # if pygame.key.get_pressed()[K_w]:
  #   y_snake = y_snake - 10
  # if pygame.key.get_pressed()[K_a]:
  #   x_snake = x_snake - 10
  # if pygame.key.get_pressed()[K_s]:
  #   y_snake = y_snake + 10
  # if pygame.key.get_pressed()[K_d]:
  #   x_snake = x_snake + 10
      

  # rect_orange = pygame.draw.rect(screen, (255, 100, 0), (200, 300, 50, 50))
  # circle_blue = pygame.draw.circle(screen, (0, 100, 255), (300, 325), 25)
  # line_green = pygame.draw.line(screen, (50, 255, 50), (350, 200), (350, 450), 5)
  # pygame.draw.line(screen, (50, 255, 50), (400, 300), (450, 300), 2)
  # pygame.draw.line(screen, (10, 255, 50), (450, 300), (450, 350), 2)
  # pygame.draw.line(screen, (50, 255, 50), (450, 350), (400, 350), 2)
  # pygame.draw.line(screen, (50, 255, 50), (400, 350), (400, 300), 2)

  # pygame.draw.rect(screen, (255, 0, 0), (500, auxY, 50, 50))
  # if auxHeigh:
  #   if auxY <= heigh_screen-50:
  #     auxY = auxY + 3
  #   else:
  #     auxHeigh = False
  # else:
  #   if auxY >= 0:
  #     auxY = auxY - 3
  #   else:
  #     auxHeigh = True
  
  head_list = []
  head_list.append(x_snake)
  head_list.append(y_snake)
  
  snake_list.append(head_list)
  add_snake(snake_list)
  
  apple = pygame.draw.rect(screen, (255, 0, 0), (x_apple, y_apple, 20, 20))
  snake = pygame.draw.rect(screen, (0, 200, 50), (x_snake, y_snake, 20, 20))
  
  if len(snake_list) > snake_length:
    del snake_list[0]
  
  if apple.colliderect(snake):
    x_apple = randint(50, 1230)
    y_apple = randint(50, 670)
    points = points + 1
    coli_sound.play()
    snake_length = snake_length + 2
    
  if snake_list.count(head_list) > 1:
    died = True
    while died:
      screen.fill((50, 0, 0))
      for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          exit()
        if event.key == K_ESCAPE:
          pygame.quit()
          exit()
        if event.type == KEYDOWN:
          if event.key == K_r:
            restart_game()
      pygame.display.update()
  
  
  screen.blit(formated_text, (1030, 30))
  pygame.display.update()
