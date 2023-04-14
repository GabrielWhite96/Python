import pygame
from pygame.locals import *
from pygame.image import load as load

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 800

MENU = load('graphic/message.png')
GAME_OVER = load('graphic/gameover.png')
BACKGROUND = load('graphic/background-day.png')
BACKGROUND_LIST = {
    'day_bg':'graphic/background-day.png',
    'night_bg':'graphic/background-night.png',
    'water_bg':'graphic/background-water.png'
}
BACKGROUND = pygame.transform.scale(BACKGROUND, (WINDOW_WIDTH, WINDOW_WIDTH))

# BACK_MUSIC = music.load('/audio/back_music.mp3')
# music.play(-1)
# music.set_volume(0.1)

# colide_sound = pygame.mixer.Sound('music/hit.wav')
# bump_sound = pygame.mixer.Sound('music/wing.wav')
# score_sound = pygame.mixer.Sound('music/score1.wav')
# colide_sound.set_volume(0.1)
# bump_sound.set_volume(0.1)
# score_sound.set_volume(0.2)

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

GROUND_WIDTH = 2 * WINDOW_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 150
