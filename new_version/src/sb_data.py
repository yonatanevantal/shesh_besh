__author__ = 'user'

# the number of game slots
NUM_SLOTS = 24 # always even

import sb_constants
from buttons import Button
# from sb_graphics import Button


"""
Represents a data of the game board.

Attributes:
    slots - a list of the slots of the board (all are GameSlot)
    cubes - a tuple of two PlayCube to roll_up a random number.
"""


class GameBoard(object):
    def __init__(self):
        self.me = Player("player1", "white")  # just starting values - will be changed after HelloClient
        self.burned_black = GameSlot(368, 600, NUM_SLOTS)
        self.burned_white = GameSlot(368, 100, NUM_SLOTS + 1)
        self.out = GameSlot(786, 1, NUM_SLOTS + 2)
        self.burned_black.button.set_size(40, 400)
        self.burned_white.button.set_size(40, 400)
        self.slots = self.init_slots()

    def __str__(self):
        ss = ""
        for s in self.slots:
            ss += " ".join([str(s.identity), str(s.pieces), s.color, "\n"])
        return ss

    # creates GameSlot and sets to them their correct location on the board. Appends them to slots.
    def init_slots(self):
        slots = []
        for i in range(NUM_SLOTS / 2):
            x = sb_constants.SEG_SLOT_X + i * sb_constants.OFFSET_SLOT_X
            y1 = sb_constants.SEG_UP_SLOT_Y
            y2 = sb_constants.SEG_DOWN_SLOT_Y

            if (i > NUM_SLOTS / 4 - 1) and (i < 3 * (NUM_SLOTS / 4) - 1):
                x += sb_constants.OFFSET_MID_SLOT_X

            slots.append(GameSlot(x, y1, i))
            slots.append(GameSlot(x, y2, NUM_SLOTS - i - 1))

        self.burned_black.color = "black"
        self.burned_white.color = "white"

        return slots

    # returns a slot by a given id
    def get_slot_by_id(self, identity):
        if identity == -1:
            return None
        if identity == 24:
            return self.burned_black
        if identity == 25:
            return self.burned_white
        if identity == 26:
            return self.out
        for s in self.slots:
            if s.identity == identity:
                return s
        return None

    # sets the number and color of pieces to each slot by the rules of shesh-besh.
    def initialize_board(self):
        for i in range(2):
            self.get_slot_by_id(0).color = "white"
            self.get_slot_by_id(0).add()
            self.get_slot_by_id(NUM_SLOTS - 1).color = "black"
            self.get_slot_by_id(NUM_SLOTS - 1).add()
        for i in range(5):
            self.get_slot_by_id(NUM_SLOTS / 4 - 1).color = "black"
            self.get_slot_by_id(NUM_SLOTS / 4 - 1).add()
            self.get_slot_by_id(3 * (NUM_SLOTS / 4)).color = "white"
            self.get_slot_by_id(3 * (NUM_SLOTS / 4)).add()
        for i in range(3):
            self.get_slot_by_id(NUM_SLOTS / 4 + 1).color = "black"
            self.get_slot_by_id(NUM_SLOTS / 4 + 1).add()
            self.get_slot_by_id(3 * (NUM_SLOTS / 4) - 2).color = "white"
            self.get_slot_by_id(3 * (NUM_SLOTS / 4) - 2).add()
        for i in range(5):
            self.get_slot_by_id(NUM_SLOTS / 2 - 1).color = "white"
            self.get_slot_by_id(NUM_SLOTS / 2 - 1).add()
            self.get_slot_by_id(NUM_SLOTS / 2).color = "black"
            self.get_slot_by_id(NUM_SLOTS / 2).add()


class Player():
    def __init__(self, name, color):
        self.color = color
        self.name = name


"""
Represents a slot on the game board.

Attributes:
    pieces - the number of pieces in the slot.
    color - the color of the pieces in the slot.
    identity - a unique number to each slot. 0-23 from up:right to down:right.
    x - a number that is used to represent the value of the piece in x axis
    y - a number that is used to represent the value of the piece in y axis
"""


class GameSlot(object):
    def __init__(self, x, y, identity):
        self.pieces = 0
        self.color = ""
        self.identity = identity
        self.x = x
        self.y = y

        if 24 > identity > 11:
            self.button = Button(x, 500, 56, 383)
        else:
            if identity == 24 or identity == 25:
                self.button = Button(x, y, 56, 383)
            else:
                self.button = Button(x, y, 900 - x, 900 - y)

    def add(self):
        self.pieces += 1

    def remove(self):
        self.pieces -= 1

    def __str__(self):
        return "~".join([str(self.pieces), self.color, str(self.x), str(self.y)])

