__author__ = 'user'

NUM_SLOTS = 24 # always even

import pos_constants
from random import randint


class GameBoard(object):
    def __init__(self):
        self.slots = []
        self.slots = self.init_slots()
        self.cubes = (PlayCube(), PlayCube())

    def init_slots(self):
        slots = []
        for i in range(NUM_SLOTS / 2):
            x = pos_constants.SEG_SLOT_X + i * pos_constants.OFFSET_SLOT_X
            y1 = pos_constants.SEG_UP_SLOT_Y
            y2 = pos_constants.SEG_DOWN_SLOT_Y

            if (i > NUM_SLOTS / 4 - 1) and (i < 3 * (NUM_SLOTS / 4) - 1):
                x += pos_constants.OFFSET_MID_SLOT_X

            slots.append(GameSlot(x, y1, i))
            slots.append(GameSlot(x, y2, NUM_SLOTS -  i - 1))
        return slots

    def get_slot_by_id(self, identity):
        for s in self.slots:
            if s.identity == identity:
                return s
        return None

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