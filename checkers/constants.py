import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
ABOUT = [f'Author: Evgeniia Buzulukova',
         f'Email: evgeniia@uni.minerva.edu']
DIFFICULTY = ['EASY']
FPS = 60
TRANSPOSITION_TABLE_FILENAME = "ttable.pkl"
GAME_NAME = 'Checkers'

# rgb
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

CROWN = pygame.transform.scale(pygame.image.load('assets/img.png'), (44, 25))
