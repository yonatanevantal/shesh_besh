__author__ = 'user'

# the number of game slots
NUM_SLOTS = 24 # always even

import sb_constants
from random import randint


"""
Represents a data of the game board.

Attributes:
    slots - a list of the slots of the board (all are GameSlot)
    cubes - a tuple of two PlayCube to roll a random number.
"""


class GameBoard(object):
    def __init__(self):
        self.slots = []
        self.slots = self.init_slots()
        self.cubes = (PlayCube(), PlayCube())
        self.me = Player("player1", "white")  # just starting values - will be changed after HelloClient

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
        return slots

    # returns a slot by a given id
    def get_slot_by_id(self, identity):
        if identity == -1:
            return None

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

    def add(self):
        self.pieces += 1

    def rem(self):
        self.pieces -= 1


class PlayCube(object):
    def __init__(self):
        self.num = 0

    def roll(self):
        self.num = randint(0, 6)