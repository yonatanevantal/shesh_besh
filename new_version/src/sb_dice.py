__author__ = 'yonatan'

import random
import pygame
import os

# the general path to the project file ('new_version')
PATH = os.path.dirname(os.path.abspath(__file__))


class Dice():
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y

        self.screen = screen
        self.num = random.randint(1, 6)  # undefined
        self.progress = 20  # at start
        self.dice_dict = {
            1: pygame.image.load(os.path.dirname(PATH).replace("new_version", r"imgs\pngs\1.png")).convert_alpha(),
            2: pygame.image.load(os.path.dirname(PATH).replace("new_version", r"imgs\pngs\2.png")).convert_alpha(),
            3: pygame.image.load(os.path.dirname(PATH).replace("new_version", r"imgs\pngs\3.png")).convert_alpha(),
            4: pygame.image.load(os.path.dirname(PATH).replace("new_version", r"imgs\pngs\4.png")).convert_alpha(),
            5: pygame.image.load(os.path.dirname(PATH).replace("new_version", r"imgs\pngs\5.png")).convert_alpha(),
            6: pygame.image.load(os.path.dirname(PATH).replace("new_version", r"imgs\pngs\6.png")).convert_alpha()
        }
        self.surf = self.dice_dict[self.num]
        self.vx = 7
        self.vy = 1

    def roll_up(self):
        self.progress = 0
        self.num = random.randint(1, 6)

    def roll_down(self):
        self.progress = 0
        self.num = random.randint(1, 6)
        self.vy = -abs(self.vy)

    def spin(self):
        self.num = random.randint(1, 6)

    def rotate(self):
        self.surf = pygame.transform.rotate(self.dice_dict[self.num], int(self.progress * 20))

    def move(self):
        self.x -= self.vx
        self.y += self.vy

    def show(self):
        if self.progress < 20:
            self.spin()
            self.rotate()
            self.move()
            self.progress +=1

        self.screen.blit(self.surf, (self.x, self.y))

    def not_rolling(self):
        return self.progress == 20

    def set_num(self, x):
        self.num = x
        self.surf = self.dice_dict[x]


def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    clock = pygame.time.Clock()
    done = False
    d = Dice(200, 150, screen)
    d2 = Dice(200, 110, screen)

    d.roll_up()
    d2.roll_down()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    done = True
        screen.fill((0, 0, 0))

        d.show()
        d2.show()

        pygame.display.flip()
        clock.tick(10)

if __name__ == "__main__":
    main()