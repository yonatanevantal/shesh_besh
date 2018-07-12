__author__ = 'user'
import pygame
from sb_graphics import *

g = Game()
g.board.initialize_board()

# g.board.slots[0].remove()
# g.board.slots[1].add()
#
# print g.board

pygame.init()
screen = pygame.display.set_mode((900, 900))
done = False

g.board.slots[0].remove()
g.board.slots[1].add()

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True


        g.update_screen()
        pygame.display.flip()
