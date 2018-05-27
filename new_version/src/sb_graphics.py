from pos_constants import SCREEN_SIZE
from pygame.locals import *
from game import *
import pygame
import sys
import os


FPS = 30


class Game(object):
    def __init__(self):
        self.board = GameBoard()
        self.image = pygame.image.load(
            os.path.dirname(os.path.abspath(__file__)).replace("src", r"imgs\pngs\game_board.png"))
        self.rect = self.image.get_rect()

    def handle_board(self):
        pygame.init()

        display = pygame.display.set_mode((0, 0), screen_mode = pygame.FULLSCREEN)

        clock = pygame.time.Clock()
        pygame.display.set_caption('Shesh Besh')

        self.board.initialize_board()

        # add showing pieces in each slot

        display.blit(self.image.convert_alpha(), self.rect)
        pygame.display.flip()

        while True:  # main game loop
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.flip()


class Piece(pygame.sprite.Sprite):
    def __init__(self, piece_data):
        pygame.sprite.Sprite.__init__(self)
        self.info = piece_data
        if self.info.color == "black":
            self.image = pygame.image.load(
                os.path.dirname(os.path.abspath(__file__)).replace("src", r"imgs\pngs\game_piece_black.png"))
        else:
            self.image = pygame.image.load(
                os.path.dirname(os.path.abspath(__file__)).replace("src", r"imgs\pngs\game_piece_white.png"))

        self.rect = self.image.get_rect()

""""
class SelectedSlot(pygame.sprite):
    pass
"""

