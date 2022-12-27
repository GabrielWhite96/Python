import pygame
from random import randint
from pygame.locals import *

clock = pygame.time.Clock()

pygame.init()

WIDTH_SCREEN = 400
HEIGHT_SCREEN = 800

screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))

pygame.display.set_caption('Flappy Bird')

BACKGROUND = pygame.image.load('assets/sprites/background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH_SCREEN, HEIGHT_SCREEN))

BACK_MUSIC = pygame.mixer.music.load('assets//audio/back_music.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

colide_sound = pygame.mixer.Sound('assets/audio/hit.wav')
bump_sound = pygame.mixer.Sound('assets/audio/wing.wav')
colide_sound.set_volume(0.1)
bump_sound.set_volume(0.1)


FALLING_SPEED = 10
GRAVITY = 1
GAME_SPEED = 5

GROUND_WIDTH = 2 * WIDTH_SCREEN
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 200

DIED = False


class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('assets//sprites//pink1.png').convert_alpha(),
                       pygame.image.load('assets//sprites//pink2.png').convert_alpha(),
                       pygame.image.load('assets//sprites//pink3.png').convert_alpha()]

        self.FALLING_SPEED = FALLING_SPEED

        self.current_image = 0

        self.image = pygame.image.load('assets//sprites//pink1.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = WIDTH_SCREEN / 2
        self.rect[1] = HEIGHT_SCREEN / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[ self.current_image ]

        self.FALLING_SPEED += GRAVITY

        # Update height
        self.rect[1] += self.FALLING_SPEED
    
    def bump(self):
        self.FALLING_SPEED = -FALLING_SPEED

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
    size = randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, HEIGHT_SCREEN - size - PIPE_GAP)
    return (pipe, pipe_inverted)

    

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

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bump_sound.play()
                bird.bump()

    screen.blit(BACKGROUND, (0, 0))

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

    bird_group.update()
    ground_group.update()
    pipe_group.update()

    bird_group.draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)

    pygame.display.update()
    
    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        # Game over
        colide_sound.play()
        DIED = True
        while DIED:
            break
        