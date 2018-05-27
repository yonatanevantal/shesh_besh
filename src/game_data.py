import pos_constants
from random import randint

NUM_SLOTS = 24
NUM_PIECES = int(30 / 2)


class GameBoard(object):
    def __init__(self):
        self.slots = []
        self.slots = self.init_slots()

        self.black_pieces = self.init_pieces("black")

        self.white_pieces = self.init_pieces("white")

        self.cubes = (PlayCube(), PlayCube())

    def init_slots(self):
        slots = []
        for i in range(NUM_SLOTS):
            """
            if i <= 11:
                slots.append(
                    GameSlot(pos_constants.SEG_SLOT_X + i * pos_constants.OFFSET_SLOT_X, pos_constants.SEG_UP_SLOT_Y,
                             i))
                pass
            else:
                slots.append(
                    GameSlot((11 - i) * pos_constants.OFFSET_SLOT_X, pos_constants.SEG_DOWN_SLOT_Y,
                             i)) """

            x = pos_constants.SEG_SLOT_X + i * pos_constants.OFFSET_SLOT_X
            y1 = pos_constants.SEG_UP_SLOT_Y
            y2 = pos_constants.SEG_DOWN_SLOT_Y

            if i > 5 and i < 17:
                x += pos_constants.OFFSET_MID_SLOT_X

            slots.append(GameSlot(x, y1, id))
            slots.append(GameSlot(x, y2, id))
        return slots

    def init_pieces(self, color):
        pieces = []
        for i in range(NUM_PIECES):
            pieces.append(GamePiece(color))
        return pieces

    # arranges the board to the game starting position
    # there are 8 places to put pieces in
    # view game starting position => http://img.brothersoft.com/screenshots/softimage/b/backgammon_classic-23005-1.jpeg
    def init(self):
        cnt = 0
        for j in range(2):
            self.slots[0].add(self.white_pieces[cnt])
            self.slots[NUM_SLOTS - 1].add(self.black_pieces[cnt])
            cnt += 1
        for j in range(5):
            self.slots[int(NUM_SLOTS / 4 - 1)].add(self.black_pieces[cnt])
            self.slots[int(NUM_SLOTS - (NUM_SLOTS / 4 - 1))].add(self.white_pieces[cnt])
            cnt += 1
        for j in range(3):
            self.slots[int(NUM_SLOTS / 4 + 1)].add(self.black_pieces[cnt])
            self.slots[int(NUM_SLOTS - (NUM_SLOTS / 4 + 1))].add(self.white_pieces[cnt])
            cnt += 1
        for j in range(5):
            self.slots[int(NUM_SLOTS / 2 - 1)].add(self.white_pieces[cnt])
            self.slots[int(NUM_SLOTS - NUM_SLOTS / 2)].add(self.black_pieces[cnt])
            cnt += 1


class GameSlot(object):
    def __init__(self, x, y, id):
        self.pieces = []
        self.id = id
        self.x = x
        self.y = y

    def add(self, new_piece):
        if self.pieces is None:
            new_piece.move(self.x, self.y)
            self.pieces.append(new_piece)
        else:
            if new_piece.is_up() or int(self.id) - 1 == 22:           # piece changes height from down to up
                new_piece.move(self.x, pos_constants.SEG_UP_SLOT_Y + len(self.pieces) * pos_constants.OFFSET_SLOT_Y)
                self.pieces.append(new_piece)
            elif not new_piece.is_up() or int(self.id) + 1 == 23:     # piece changes height from up to down
                new_piece.move(self.x, pos_constants.SEG_DOWN_SLOT_ - len(self.pieces) * pos_constants.OFFSET_SLOT_Y)
                self.pieces.append(new_piece)
            else:
                pass                                                  # must enter in ifs above

    def rem(self):
        tmp = self.pieces[len(self.pieces) - 1]
        self.pieces.remove()
        return tmp


class GamePiece(object):
    def __init__(self, color, x = 0, y = 0):
        self.x = x
        self.y = y
        self.color = color

    def move(self, x, y):
        self.x = x
        self.y = y

    def is_up(self):
        if self.y <= pos_constants.SCREEN_SIZE[1] / 2:
            return True
        return False

class PlayCube(object):
    def __init__(self):
        self.num = 0

    def roll(self):
        self.num = randint(0, 6)