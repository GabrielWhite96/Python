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

width_screen = 400
heigh_screen = 440

font = pygame.font.SysFont('arial', 20, True, False)
points = 0
high_points = 0

clock = pygame.time.Clock()

snake_length = 5

died = False

snake_list = []

font_2 = pygame.font.SysFont('arial', 20, True, True)
died_msg = "Game Over! Pressione a tecla R para jogar novamente ou ESQ para sair"
formated_die_text = font_2.render(died_msg, True, (255, 255, 255))
rect_text = formated_die_text.get_rect()

speed = 20
x_control = speed
y_control = 0
x_snake = int((width_screen/2)//20*20)
y_snake = int((heigh_screen/2)//20*20)
x_apple = randint(0, 380)//20 * 20
y_apple = randint(40, 420)//20 * 20

def add_snake(snake_list):
  for XandY in snake_list:
    pygame.draw.rect(screen, (0, 200, 50), (XandY[0],XandY[1] , 20, 20))


def restart_game():
  global points, snake_length, x_snake, y_snake, x_apple, y_apple, head_list, snake_list, died, x_control, y_control
  points = 0
  snake_length = 5
  x_snake = int(width_screen/2)
  y_snake = int(heigh_screen/2)
  x_apple = randint(0, 380)//20 * 20
  y_apple = randint(40, 420)//20 * 20
  head_list = []
  snake_list = []
  died = False
  x_control = speed
  y_control = 0

screen = pygame.display.set_mode((width_screen, heigh_screen))

while True:
  screen.fill((0, 0, 0))
  clock.tick(10)
  
  msg_points = f'Pontos: {points}'
  msg_high_points = f'Maior Pontuação-: {high_points}'
  formated_text = font.render(msg_points, True, (255, 255, 255))
  
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      exit()
      
    if event.type == KEYDOWN:
      if event.key == K_ESCAPE:
        pygame.quit()
        exit()
      if event.key == K_UP:
        if y_control == speed:
          pass
        else:
          x_control = 0
          y_control = -speed
      if event.key == K_LEFT:
        if x_control == speed:
          pass
        else:
          x_control = -speed
          y_control = 0
      if event.key == K_DOWN:
        if y_control == -speed:
          pass
        else:
          x_control = 0
          y_control = speed
      if event.key == K_RIGHT:
        if x_control == -speed:
          pass
        else:
          x_control = speed
          y_control = 0
    
  x_snake = x_snake + x_control
  y_snake = y_snake + y_control
  
  head_list = []
  head_list.append(x_snake)
  head_list.append(y_snake)
  
  snake_list.append(head_list)
  add_snake(snake_list)
  
  pygame.draw.line(screen, (255, 255, 255), (0, 40), (width_screen, 40))
  apple = pygame.draw.rect(screen, (255, 0, 0), (x_apple, y_apple, 20, 20))
  snake = pygame.draw.rect(screen, (0, 200, 50), (x_snake, y_snake, 20, 20))
  
  if len(snake_list) > snake_length:
    del snake_list[0]
  
  if apple.colliderect(snake):
    x_apple = randint(0, 380)//20 * 20
    y_apple = randint(40, 420)//20 * 20
    for XY in snake_list:
      if x_apple == XY[0]:
        x_apple = randint(0, 380)//20 * 20
      if y_apple == XY[1]:
        y_apple = randint(40, 380)//20 * 20
    points = points + 1
    coli_sound.play()
    snake_length = snake_length + 2
    
  if head_list[0] > 380 or head_list[0] < 0 or head_list[1] > 420 or head_list[1] < 40:
    died = True
    
  
  if snake_list.count(head_list) > 1:
    died = True
    
  while died:
    screen.fill((50, 0, 0))
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        exit()
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          pygame.quit()
          exit()
        if event.key == K_r:
          restart_game()
    rect_text.center = (width_screen//2, heigh_screen//2)
    screen.blit(formated_die_text, (rect_text))
    pygame.display.update()
  
  
  screen.blit(formated_text, (10, 10))
  pygame.display.update()
