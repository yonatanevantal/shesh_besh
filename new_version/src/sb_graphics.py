from sb_constants import SCREEN_SIZE
from pygame.locals import *
from buttons import Button, ImageButton
from sb_dice import Dice
from sb_data import *
import webbrowser
import threading
# import sb_server
import pygame
import sys
import os


add_to_log = threading.Lock()

# the frame rate of the game
FPS = 30

# the general path to the project file ('new_version')
PATH = os.path.dirname(os.path.abspath(__file__))

# the image of the window icon
icon = pygame.image.load(os.path.dirname(PATH).replace("new_version", r"imgs\pngs\shesh_besh_icon.png"))

# a link to a site which explains the rules of shesh-besh
instructions = 'http://www.bkgm.com/variants/SheshBesh.html'


def get_logged_total_clients():
    with add_to_log:
        with open(sb_constants.LOG_FILE, 'rb+') as f:
            tc = f.read()
        if tc == "":
            return sb_constants.NUM_CLIENTS
        return int(tc)

"""
Represents a game of shesh-besh.
Uses graphic methods and classes.
Also, uses sb_data to handle complex data structures.

Attributes:
    display - the screen of the game. Used to show and change the screen.
    clock - used to match graphic movement and current PC timer.
    background - a surface which is the background of the game.
    rect(?)
    board - an object that is used to handle the data of a certain board situation.
            Also, used to arrange the data of the game.
"""


class Game(object):
    def __init__(self):
        self.display = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()

        self.background = pygame.image.load("imgs\\pngs\\game_board.png")
        self.start_menu = pygame.image.load("imgs\\pngs\\intro_menu.png")
        self.piece_glow = pygame.image.load("imgs\\pngs\\game_piece_glow.png")
        self.waiting_screen = pygame.image.load("imgs\\pngs\\waiting_screen.png")
        self.roll_button_released = pygame.image.load("imgs\\pngs\\roll_button.jpg")
        self.roll_button_pressed = pygame.image.load("imgs\\pngs\\roll_button_shadow.jpg")
        self.roll_button = ImageButton(self.display, 340, 400, self.roll_button_released, self.roll_button_pressed)

        self.board = GameBoard()

        self.dice = (Dice(SCREEN_SIZE[0] / 4, SCREEN_SIZE[1] / 2, self.display),
                     Dice(SCREEN_SIZE[0] / 4, SCREEN_SIZE[1] / 2 - 60, self.display))

    def reset_dice(self):
        self.dice[0].x = sb_constants.DICE_INIT_LOC[0]
        self.dice[0].y = sb_constants.DICE_INIT_LOC[1]
        self.dice[1].x = sb_constants.DICE_INIT_LOC[0]
        self.dice[1].y = sb_constants.DICE_INIT_LOC[1] - 60
        # return self.dice

    def handle_menu_clicks(self, mouse):
        play_click = self.play_button()
        instr_click = self.instructions_button(mouse)
        if play_click:
            return 1
        elif instr_click:
            return 2

    def play_button(self):
        if pygame.mouse.get_pressed()[0] == 1:
            correct_x = (pygame.mouse.get_pos()[0] > sb_constants.PLAY_BUTTON_X_1) and (pygame.mouse.get_pos()[0] < sb_constants.PLAY_BUTTON_X_2)
            correct_y = (pygame.mouse.get_pos()[1] > sb_constants.PLAY_BUTTON_Y_1) and (pygame.mouse.get_pos()[1] < sb_constants.PLAY_BUTTON_Y_2)
            if correct_x and correct_y:
                return True
            return False

    def instructions_button(self, mouse):
        if mouse.get_pressed()[0] == 1:
            correct_x_1 = (mouse.get_pos()[0] > sb_constants.INSTR_BUTTON_X_1[0]) and (mouse.get_pos()[0] < sb_constants.INSTR_BUTTON_X_1[1])
            correct_x_2 = (mouse.get_pos()[0] > sb_constants.INSTR_BUTTON_X_2[0]) and (mouse.get_pos()[0] < sb_constants.INSTR_BUTTON_X_2[1])
            correct_y_1 = (mouse.get_pos()[1] > sb_constants.INSTR_BUTTON_Y_1[0]) and (mouse.get_pos()[1] < sb_constants.INSTR_BUTTON_Y_1[1])
            correct_y_2 = (mouse.get_pos()[1] > sb_constants.INSTR_BUTTON_Y_2[0]) and (mouse.get_pos()[1] < sb_constants.INSTR_BUTTON_Y_2[1])
            if (correct_x_1 and correct_y_1) ^ (correct_x_2 and correct_y_2):
                return True
            return False

    def set_board(self):
        all_pieces = self.draw_pieces_in_all_slots()
        return all_pieces

    def init_window(self):
        pygame.init()
        pygame.display.set_caption('Shesh Besh')
        pygame.display.set_icon(icon)

    @staticmethod
    def open_instructions():
        webbrowser.open(instructions)

    def start_menu_clicks(self, mouse, is_first):
        click_status = self.handle_menu_clicks(mouse)
        if click_status == 1:
            if is_first:
                self.display.blit(self.waiting_screen.convert(), self.waiting_screen.get_rect())
            else:
                self.display.blit(self.background.convert(), self.background.get_rect())
        elif click_status == 2:
            Game.open_instructions(instructions)
        return click_status
    """
    def handle_wait_for_opponent(self, total_clients):
        if total_clients == 1:
            self.display.blit(self.)
    """
    def handle_start_menu(self, is_first):
        click_status = 0
        while click_status != 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                click_status = self.start_menu_clicks(pygame.mouse, is_first)  # might be None

            pygame.display.flip()

    def handle_board(self):
        self.init_window()
        self.board.initialize_board()

        self.display.blit(self.start_menu, self.start_menu.get_rect())

        if get_logged_total_clients() == 1:
            self.handle_start_menu(True)
            while get_logged_total_clients() == 1:
                pass
            self.display.blit(self.background.convert(), self.background.get_rect())
        else:
            self.handle_start_menu(False)

        pieces = self.set_board()
        pygame.display.flip()

        while True:  # main game loop
            events = pygame.event.get()
            for event in events:
                mouse = pygame.mouse

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.update_screen()
            self.roll_button.show()
            if self.roll_button.is_pressed(events):
                self.dice[0].roll_up()
                self.dice[1].roll_down()
            self.dice[0].show()
            self.dice[1].show()

                # self.handle_slots_clicks(mouse)

            pygame.display.flip()
            self.clock.tick(FPS)

    def draw_slots(self):
        black = Piece("black")
        white = Piece("white")
        for slot in self.board.slots:
            for i in xrange(slot.pieces):
                if slot.color == "black":
                    if slot.identity < 12:
                        self.display.blit(black.image, (slot.x, slot.y + i * black.image.get_height()))
                    else:
                        self.display.blit(black.image, (slot.x, slot.y - i * black.image.get_height()))
                else:
                    if slot.identity < 12:
                        self.display.blit(white.image, (slot.x, slot.y + i * white.image.get_height()))
                    else:
                        self.display.blit(white.image, (slot.x, slot.y - i * white.image.get_height()))
        for i in xrange(self.board.burned_black.pieces):
            self.display.blit(black.image, (self.board.burned_black.x, self.board.burned_black.y - i * black.image.get_height()))
        for i in xrange(self.board.burned_white.pieces):
            self.display.blit(white.image, (self.board.burned_white.x, self.board.burned_white.y - i * white.image.get_height()))


    def update_screen(self):
        self.display.blit(self.background.convert(), self.background.get_rect())
        self.draw_slots()

    def handle_slots_clicks(self, mouse):
        clicked_slot = self.get_clicked_slot(mouse)
        if clicked_slot is not None:
            self.highlight_slot(clicked_slot)

    def highlight_slot(self, slot):
        pos = self.get_slot_pos(slot)
        if pos is not None:
            self.display.blit(self.piece_glow.convert_alpha(), self.piece_glow.get_rect().move(pos))

    def cover_highlight_slot(self, slot):
        x, y = self.get_slot_pos(slot)
        if slot.color == "white":
            p = Piece("white")
            self.display.blit(p.image, p.image.get_rect().move(x, y))
        else:
            p = Piece("black")
            self.display.blit(p.image, p.image.get_rect().move(x, y))

    def get_slot_pos(self, slot):
        try:
            if slot.pieces != 0 and slot.color == self.board.me.color:
                x = slot.x
                if slot.identity <= (NUM_SLOTS / 2 - 1):
                    y = slot.y + sb_constants.OFFSET_SLOT_Y * (slot.pieces - 1)
                else:
                    y = slot.y - sb_constants.OFFSET_SLOT_Y * (slot.pieces - 1)
                return x, y
        except Exception as err:
            print err.args
            print "You cannot play with your rival's pieces..."
            return

    def get_clicked_slot(self, events):
        slot_num = -1
        if self.board.burned_white.button.is_pressed(events):
            return self.board.burned_white, self.board.burned_white.identity

        if self.board.burned_black.button.is_pressed(events):
            return self.board.burned_black, self.board.burned_black.identity

        if self.board.out.button.is_pressed(events):
            return self.board.out, self.board.out.identity

        for slot in self.board.slots:
            if slot.button.is_pressed(events):
                slot_num_x = -1
                x, y = pygame.mouse.get_pos()
                if (x > sb_constants.LEFT_X[0]) and (x < sb_constants.LEFT_X[1]):
                    slot_num_x = int((x-sb_constants.LEFT_X[0])/((sb_constants.LEFT_X[1] - 10)/sb_constants.NUM_SLOTS_IN_QUARTER)) + 1
                elif (x > sb_constants.RIGHT_X[0]) and (x < sb_constants.RIGHT_X[1]):
                    slot_num_x = int((x-sb_constants.RIGHT_X[0])/((sb_constants.LEFT_X[1] - 10)/sb_constants.NUM_SLOTS_IN_QUARTER)) + 7

                if (y > sb_constants.UP_Y[0]) and (y < sb_constants.UP_Y[1]):
                    slot_num = 12 - slot_num_x
                elif (y > sb_constants.DOWN_Y[0]) and (y < sb_constants.DOWN_Y[1]):
                    slot_num = 11 + slot_num_x

                return self.board.get_slot_by_id(slot_num), slot_num

        return None, -1

"""
Represents a game piece in the game, in the graphical way.
Inherit from Sprite to make movement and graphics easier and cleaner.

Attributes:
    image - the image of the piece depends on which color is given in the constructor.
    rect(?)
    x - a number that is used to represent the value of the piece in x axis
    y - a number that is used to represent the value of the piece in y axis
"""


class Piece(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)

        self.color = color
        if self.color is "black":
            self.image = pygame.image.load(
                os.path.dirname(PATH).replace("new_version", r"imgs\pngs\game_piece_black.png"))
        else:
            self.image = pygame.image.load(
                os.path.dirname(PATH).replace("new_version", r"imgs\pngs\game_piece_white.png"))

        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0

    # to a given number, returns a list of pieces which is in the number length
    @staticmethod
    def generate_num_pieces(color, num):
        return [Piece(color) for i in range(num)]
