from pos_constants import SCREEN_SIZE
from pygame.locals import *
from game_data import *
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
        self.bp, self.wp = self.init_pieces()

    def init_pieces(self):
        bp = []
        wp = []
        for p in self.board.black_pieces:
            bp.append(Piece(p))
        for p in self.board.white_pieces:
            wp.append(Piece(p))
        return bp, wp

    def handle_board(self):
        pygame.init()

        display = pygame.display.set_mode(SCREEN_SIZE)

        clock = pygame.time.Clock()
        pygame.display.set_caption('Shesh Besh')

        self.board.init()
        display.blit(self.image.convert_alpha(), self.rect)
        for p in self.bp:
            display.blit(p.image.convert_alpha(),
                         pygame.Rect(p.info.x, p.info.y, self.image.get_rect()[0], self.image.get_rect()[1]))
        for p in self.wp:
            display.blit(p.image.convert_alpha(),
                         pygame.Rect(p.info.x, p.info.y, self.image.get_rect()[0], self.image.get_rect()[1]))
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

