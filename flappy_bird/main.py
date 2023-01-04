import pygame
from random import randint
from pygame.locals import *

clock = pygame.time.Clock()

pygame.init()

WIDTH_SCREEN = 400
HEIGHT_SCREEN = 800

screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))

pygame.display.set_caption('Flappy Bird')

MENU = pygame.image.load('assets/sprites/message.png')
GAME_OVER = pygame.image.load('assets/sprites/gameover.png')
BACKGROUND = pygame.image.load('assets/sprites/background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH_SCREEN, HEIGHT_SCREEN))

# BACK_MUSIC = pygame.mixer.music.load('assets//audio/back_music.mp3')
# pygame.mixer.music.play(-1)
# pygame.mixer.music.set_volume(0.1)

colide_sound = pygame.mixer.Sound('assets/audio/hit.wav')
bump_sound = pygame.mixer.Sound('assets/audio/wing.wav')
colide_sound.set_volume(0.1)
bump_sound.set_volume(0.1)

START = False
PERSONALIZE = False
DIED = False
FALLING_SPEED = 10
GRAVITY = 1
GAME_SPEED = 5

GROUND_WIDTH = 2 * WIDTH_SCREEN
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 200

class Personalize_game(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Personalize_button(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/sprites/personalizar_button.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (156, 40))
        self.rect = self.image.get_rect()
        
        
        
    def update(self):
        global PERSONALIZE
        self.mouse = pygame.mouse.get_pressed()
        self.mousePos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(self.mousePos):
            if self.mouse[0]:
                PERSONALIZE = True
        
class Point(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.images = [pygame.image.load('assets/sprites/0.png'),
                       pygame.image.load('assets/sprites/1.png'),
                       pygame.image.load('assets/sprites/2.png'),
                       pygame.image.load('assets/sprites/3.png'),
                       pygame.image.load('assets/sprites/4.png'),
                       pygame.image.load('assets/sprites/5.png'),
                       pygame.image.load('assets/sprites/6.png'),
                       pygame.image.load('assets/sprites/7.png'),
                       pygame.image.load('assets/sprites/8.png'),
                       pygame.image.load('assets/sprites/9.png')]
        
        self.current_image = 0
        self.point_aux = 0
        
        self.image = pygame.image.load('assets/sprites/0.png')
        
        self.rect = self.image.get_rect()
        self.rect[0] = WIDTH_SCREEN / 4
        
    def update(self):
        self.current_image = self.current_image + 1
        self.image = self.images[ self.current_image ]
        if self.current_image == 9:
            self.point_aux = self.point_aux + 1
        
class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('assets//sprites//white1.png').convert_alpha(),
                       pygame.image.load('assets//sprites//white2.png').convert_alpha(),
                       pygame.image.load('assets//sprites//white3.png').convert_alpha()]

        self.FALLING_SPEED = FALLING_SPEED

        self.current_image = 0

        self.image = pygame.image.load('assets//sprites//white1.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = WIDTH_SCREEN / 2 - 17
        self.rect[1] = HEIGHT_SCREEN / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[ self.current_image ]
        self.image = pygame.transform.rotate(self.image, -1.5 * self.FALLING_SPEED)

        self.FALLING_SPEED += GRAVITY

        # Update height
        self.rect[1] += self.FALLING_SPEED
            
    def bump(self):
        self.FALLING_SPEED = -1.4 *FALLING_SPEED

class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets//sprites//pipe-black.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH,PIPE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = HEIGHT_SCREEN - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED

class Ground(pygame.sprite.Sprite):
    
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets//sprites//base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = HEIGHT_SCREEN - GROUND_HEIGHT
    
    def update(self):
        self.rect[0] -= GAME_SPEED

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(xpos):
    size = randint(150, 600)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, HEIGHT_SCREEN - size - PIPE_GAP)
    return (pipe, pipe_inverted)

# point_group = pygame.sprite.Group()
# for i in range(2):
#     point = Point()
#     point_group.add(point[0])
#     point_group.add(point[1])

personalize_button_group = pygame.sprite.Group()
personalize_button = Personalize_button()
personalize_button_group.add(personalize_button)

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDTH * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(WIDTH_SCREEN * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

def restart_game():
    global bird_group, ground_group, pipe_group, bird, ground, pipes, DIED, START, personalize_button, personalize_button_group
    
    bird_group.empty()
    ground_group.empty()
    pipe_group.empty()
    
    personalize_button = Personalize_button()
    personalize_button_group.add(personalize_button)
    bird = Bird()
    bird_group.add(bird)

    for i in range(2):
        ground = Ground(GROUND_WIDTH * i)
        ground_group.add(ground)

    for i in range(2):
        pipes = get_random_pipes(WIDTH_SCREEN * i + 800)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])
    
    DIED = False
    START = False

while True:
    clock.tick(30)
    screen.blit(BACKGROUND, (0, 0))
        
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                START = True
                bump_sound.play()
                bird.bump()
                
    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)

    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])

        pipes = get_random_pipes(WIDTH_SCREEN * 2 - 30)

        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])
        
    pipe_group.draw(screen)
    ground_group.draw(screen)
    personalize_button_group.draw(screen)
    personalize_button_group.update()
    
    if START:
        personalize_button_group.empty()
        
        bird_group.update()
        ground_group.update()
        pipe_group.update()

        bird_group.draw(screen)
    else:
        if PERSONALIZE:
            screen.fill((255,255,255))
            
        else:
            screen.blit(MENU, ((WIDTH_SCREEN/2)-92, (HEIGHT_SCREEN/2)-150))
        
    pygame.display.update()
    
    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        colide_sound.play()
        DIED = True
    
    while DIED:
        pygame.display.update()
        screen.blit(GAME_OVER, ((WIDTH_SCREEN/2)-96, (HEIGHT_SCREEN/2)-60))
        # restart_game()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == K_SPACE:
                    restart_game()
                    
            
        