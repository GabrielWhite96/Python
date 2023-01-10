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
score_sound = pygame.mixer.Sound('assets/audio/score1.wav')
colide_sound.set_volume(0.1)
bump_sound.set_volume(0.1)
score_sound.set_volume(0.2)

START = False
PERSONALIZE = False
PERSONALIZE_BIRD = False
BLACK_BIRD = False
WHITE_BIRD = False
PINK_BIRD = False
COLOR_BIRD = 'white'
PERSONALIZE_BACKGROUND = False
DIED = False
FALLING_SPEED = 10
GRAVITY = 1.4
GAME_SPEED = 5

GROUND_WIDTH = 2 * WIDTH_SCREEN
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 150

class Color_bird(pygame.sprite.Sprite):
    
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('assets/sprites/'+color+'_bird.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        
        self.color = color
        self.rect[0] = width
        self.rect[1] = height
        
    def update(self):
        global COLOR_BIRD, PERSONALIZE, PERSONALIZE_BIRD
        
        self.mouse = pygame.mouse.get_pressed()
        self.mousePos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(self.mousePos):
            if self.mouse[0]:
                COLOR_BIRD = self.color
                PERSONALIZE = False
                PERSONALIZE_BIRD = False

class Personalize_bird(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('assets/sprites/bird.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        
        self.rect[0] = 80
        self.rect[1] = 150
        
    def update(self):
        global PERSONALIZE_BIRD
        
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
            PERSONALIZE_BIRD = True

class Personalize_background(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('assets/sprites/background.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        
        self.rect[0] = WIDTH_SCREEN - 180
        self.rect[1] = 150
        
    def update(self):
        global PERSONALIZE_BACKGROUND
        
        self.mouse = pygame.mouse.get_pressed()
        self.mousePos = pygame.mouse.get_pos()           
        
        if self.rect.collidepoint(self.mousePos):
            if self.mouse[0]:
                PERSONALIZE_BACKGROUND = True

class Personalize_button(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/sprites/personalizar_button.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (156, 40))
        self.rect = self.image.get_rect()
        
        self.rect[0] = 10
        self.rect[1] = 10
        
    def update(self):
        global PERSONALIZE
        
        self.mouse = pygame.mouse.get_pressed()
        self.mousePos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(self.mousePos):
            if self.mouse[0]:
                PERSONALIZE = True
        
class Score(pygame.sprite.Sprite):
    
    def __init__(self, width, height, first, second, third):
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
        
        # self.current_image = 0
        self.score_cont = 0
        self.score_aux1 = 0
        self.score_aux2 = 0
        self.score_aux3 = 0
        
        self.first_number = first
        self.second_number = second
        self.third_number = third
        
        self.image = pygame.image.load('assets/sprites/0.png')
        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_rect()
        self.rect[0] = width
        self.rect[1] = height
        
    def update(self):
        # self.current_image += 1
        # self.image = self.images[ self.current_image ]
        self.score_cont += 1
        
        if self.first_number:
            if self.score_cont%100 == 0:
                self.score_aux1 += 1
                if self.score_aux1 == 10:
                    self.score_aux1 = 0
                self.image = self.images[self.score_aux1]
                
        if self.second_number:
            if self.score_cont%10 == 0:                    
                self.score_aux2 += 1
                if self.score_aux2 == 10:
                    self.score_aux2 = 0
                self.image = self.images[self.score_aux2]
                
        if self.third_number:
            self.score_aux3 += 1
            self.image = self.images[self.score_aux3]
            if self.score_aux3 == 9:
                    self.score_aux3 = -1
        

def select_bird():
    if COLOR_BIRD == 'white':
        return [pygame.image.load('assets//sprites//white1.png').convert_alpha(),pygame.image.load('assets//sprites//white2.png').convert_alpha(),pygame.image.load('assets//sprites//white3.png').convert_alpha()]
    elif COLOR_BIRD == 'black':
        return [pygame.image.load('assets//sprites//black1.png').convert_alpha(),pygame.image.load('assets//sprites//black2.png').convert_alpha(),pygame.image.load('assets//sprites//black3.png').convert_alpha()]
    elif COLOR_BIRD == 'pink':
        return [pygame.image.load('assets//sprites//pink1.png').convert_alpha(),pygame.image.load('assets//sprites//pink2.png').convert_alpha(),pygame.image.load('assets//sprites//pink3.png').convert_alpha()]
    elif COLOR_BIRD == 'green':
        return [pygame.image.load('assets//sprites//green1.png').convert_alpha(),pygame.image.load('assets//sprites//green2.png').convert_alpha(),pygame.image.load('assets//sprites//green3.png').convert_alpha()]
        
class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = select_bird()

        self.FALLING_SPEED = FALLING_SPEED

        self.current_image = 0

        self.image = pygame.image.load('assets//sprites//white1.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = WIDTH_SCREEN / 2 - 17
        self.rect[1] = HEIGHT_SCREEN / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
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

def position(sprite):
    return sprite.rect[0]

def get_random_pipes(xpos):
    size = randint(150, 600)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, HEIGHT_SCREEN - size - PIPE_GAP)
    return (pipe, pipe_inverted)

score_group = pygame.sprite.Group()
first_number = Score((WIDTH_SCREEN/2-40), 10, True, False, False)
score_group.add(first_number)
second_number = Score((WIDTH_SCREEN/2-12), 10, False, True, False)
score_group.add(second_number)
third_number = Score((WIDTH_SCREEN/2+16), 10, False, False, True)
score_group.add(third_number)

color_bird_group = pygame.sprite.Group()
color_bird_white = Color_bird('white', WIDTH_SCREEN/4-25, 100)
color_bird_group.add(color_bird_white)
color_bird_black = Color_bird('black', (WIDTH_SCREEN/4)*3-75, 100)
color_bird_group.add(color_bird_black)
color_bird_pink = Color_bird('pink', WIDTH_SCREEN/4-25, 250)
color_bird_group.add(color_bird_pink)
color_bird_green = Color_bird('green', (WIDTH_SCREEN/4)*3-75, 250)
color_bird_group.add(color_bird_green)

personalize_button_group = pygame.sprite.Group()
personalize_button = Personalize_button()
personalize_button_group.add(personalize_button)

personalize_bird_group = pygame.sprite.Group()
personalize_bird = Personalize_bird()
personalize_bird_group.add(personalize_bird)

personalize_background_group = pygame.sprite.Group()
personalize_background = Personalize_background()
personalize_background_group.add(personalize_background)

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
    global bird_group, ground_group, pipe_group, bird, ground, pipes, DIED, START, GAME_SPEED, personalize_button, personalize_button_group
    
    bird_group.empty()
    ground_group.empty()
    pipe_group.empty()
    score_group.empty()
    
    first_number = Score((WIDTH_SCREEN/2-40), 10, True, False, False)
    score_group.add(first_number)
    second_number = Score((WIDTH_SCREEN/2-12), 10, False, True, False)
    score_group.add(second_number)
    third_number = Score((WIDTH_SCREEN/2+16), 10, False, False, True)
    score_group.add(third_number)
    
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
    GAME_SPEED = 5

# pygame.time.set_timer(pygame.USEREVENT, 10000)

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
                
        # if event.type == pygame.USEREVENT:
        #     GAME_SPEED += 1
                
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
        
    if position(pipe_group.sprites()[0]) == (WIDTH_SCREEN/2-40):
        score_group.update()
        score_sound.play() 
    
    pipe_group.draw(screen)
    ground_group.draw(screen)
    personalize_button_group.draw(screen)
    personalize_button_group.update()
    
    if START:
        personalize_button_group.empty()
        
        bird_group.update()
        ground_group.update()
        pipe_group.update()

        score_group.draw(screen)
        bird_group.draw(screen)
        score_group.draw(screen)
    else:
        if PERSONALIZE:
            personalize_button_group.empty()
            personalize_bird_group.draw(screen)
            personalize_background_group.draw(screen)
            personalize_bird_group.update()
            personalize_background_group.update()
            
            if PERSONALIZE_BIRD:
                personalize_bird_group.empty()
                personalize_background_group.empty()
                
                color_bird_group.draw(screen)
                color_bird_group.update()
                if not PERSONALIZE:
                    bird_group.empty()
                    bird = Bird()
                    bird_group.add(bird)
                    personalize_button = Personalize_button()
                    personalize_button_group.add(personalize_button)
                    personalize_bird = Personalize_bird()
                    personalize_bird_group.add(personalize_bird)
                    personalize_background = Personalize_background()
                    personalize_background_group.add(personalize_background)
                
            elif PERSONALIZE_BACKGROUND:
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
                    
            
        