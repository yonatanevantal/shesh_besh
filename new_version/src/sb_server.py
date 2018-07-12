import socket
import threading
import sb_constants
from sys import argv
from sb_data import *
import time
import pickle
from states import State

LOG = True
ply_num = 2
total_clients = 0
father_going_to_close = False
__author__ = 'yonatan'

# add locks as needed
add_to_log = threading.Lock()
get_player_num = threading.Lock()
change_total_clients = threading.Lock()

threads = []
turn = "player1"
dice = None
board = GameBoard()
board.initialize_board()


class ClientThread(threading.Thread):
    def __init__(self, ip, port, conn, tid):
        global ply_num
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn
        self.tid = tid
        self.end = False
        self.name = "player" + str(ply_num % 2 + 1)
        ply_num += 1

    def other(self):
        if self.name[-1] == '1':
            return "player2"
        return "player1"

    def turn_is_yours(self):
        global turn
        return turn == self.name

    def change_turn(self):
        global turn
        turn = self.other()

    def get_tuple_from_msg(self, data):
        return data.split("~")[1:3]

    def check_entry(self, dice_list):
        my_color = sb_constants.players_colors[self.name]
        if my_color == "black":
            if board.burned_black.pieces != 0:
                for die in dice_list:
                    temp_slot = board.get_slot_by_id(NUM_SLOTS - int(die))
                    if temp_slot.pieces < 2 or temp_slot.color == "black":
                        return True
                return False
        else:
            if board.burned_white.pieces != 0:
                for die in dice_list:
                    temp_slot = board.get_slot_by_id(int(die) - 1)
                    if temp_slot.pieces < 2 or temp_slot.color == "white":
                        return True
                return False
        return True

    def is_legal(self, move_data, dice_list):
        print "_____________"
        src_id = int(move_data.split("~")[1])
        dst_id = int(move_data.split("~")[2])

        print "0"

        if (src_id == 24 and dst_id == 25) or (src_id == 25 and dst_id == 24):
            return False
        if src_id == 24:
            src = board.burned_black
            dst = board.get_slot_by_id(int(dst_id))
        elif src_id == 25:
            src = board.burned_white
            dst = board.get_slot_by_id(int(dst_id))
        elif dst_id == 24:
            src = board.get_slot_by_id(int(src_id))
            dst = board.burned_black
        elif dst_id == 25:
            src = board.get_slot_by_id(int(src_id))
            dst = board.burned_white
        elif dst_id == 26:
            src = board.get_slot_by_id(int(src_id))
            dst = board.out
        else:
            src = board.get_slot_by_id(int(src_id))
            dst = board.get_slot_by_id(int(dst_id))

        my_color = sb_constants.players_colors[self.name]

        if src.color != my_color:
            return False
        if dst.color != my_color and dst.pieces > 1:
            return False

        print 0.5

        if src_id == 24:
            if board.burned_black.pieces == 0:
                return False
        if src_id == 25:
            if board.burned_white.pieces == 0:
                return False
        print 0.75

        if dst_id == 24:
            return False
        if dst_id == 25:
            return False
        if src.pieces == 0:
            return False
        print 1
        if my_color == "black":
            if board.burned_black.pieces != 0:
                if src_id != 24:
                    return False

                temp_move = False
                for die in dice_list:
                    if NUM_SLOTS - int(die) == dst_id:
                        dice_list.remove(die)
                        temp_move = True
                        break
                if not temp_move:
                    return False

            # putting out pieces handling
            if dst_id == 26:  # means you want to put out
                for i in range(6, 24):
                    if board.get_slot_by_id(i).color == "black" or board.burned_black.pieces != 0:
                        return False
                temp_out = False
                for die in dice_list:
                    if int(die) - 1 == src_id:
                        dice_list.remove(die)
                        temp_out = True
                        break
                if not temp_out:
                    return False
            print 2
        else:
            if board.burned_white.pieces != 0:
                if src_id != 25:
                    return False
                temp_move = False
                for die in dice_list:
                    if int(die) - 1 == dst_id:
                        dice_list.remove(die)
                        temp_move = True
                        break
                if not temp_move:
                    return False

            # putting out pieces handling
            if dst_id == 26:  # means you want to put out
                for i in range(0, 18):
                    if board.get_slot_by_id(i).color == "white" or board.burned_white.pieces != 0:
                        return False
                temp_out = False
                for die in dice_list:
                    if NUM_SLOTS - int(die) == src_id:
                        dice_list.remove(die)
                        temp_out = True
                        break
                if not temp_out:
                    return False
        print 3
        if board.burned_black.pieces == 0 and board.burned_white.pieces == 0:
            direction = 1
            if my_color == "black":
                direction = -1

            temp_move = False
            for die in dice_list:
                if src_id + int(die) * direction == dst_id:
                    dice_list.remove(die)
                    temp_move = True
                    break
            if not temp_move:
                return False

        print 4

        return True

    def change_board(self, move_data):
        global board

        src = move_data.split("~")[1]
        dst = move_data.split("~")[2]

        if src == "24":
            src_slot = board.burned_black
            dst_slot = board.get_slot_by_id(int(dst))
        elif src == "25":
            src_slot = board.burned_white
            dst_slot = board.get_slot_by_id(int(dst))
        elif dst == "24":
            src_slot = board.get_slot_by_id(int(src))
            dst_slot = board.burned_black
        elif dst == "25":
            src_slot = board.get_slot_by_id(int(src))
            dst_slot = board.burned_white
        elif dst == "26":
            src_slot = board.get_slot_by_id(int(src))
            dst_slot = board.out
        else:
            src_slot = board.get_slot_by_id(int(src))
            dst_slot = board.get_slot_by_id(int(dst))

        if src_slot.pieces == 0:
            src_slot.color = ""
        if dst_slot.pieces == 0:
            dst_slot.color = src_slot.color
        if dst_slot.pieces == 1 and dst_slot.color != src_slot.color:
            if dst_slot.color == "black":
                src_slot.remove()
                dst_slot.remove()
                board.burned_black.add()
                dst_slot.add()
                dst_slot.color = "white"
            else:
                src_slot.remove()
                dst_slot.remove()
                board.burned_white.add()
                dst_slot.add()
                dst_slot.color = "black"
        else:
            src_slot.remove()
            dst_slot.add()

    def pickled_board(self):
        return pickle.dumps(board)

    def check_win(self):
        recv = self.conn.recv(1024)  # wait for client to ask
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", recv
        you_win = True
        other_win = True
        for slot in board.slots:
            if slot.color == sb_constants.players_colors[self.name] and slot.pieces != 0:
                you_win = False
            if slot.color == sb_constants.players_colors[self.other()] and slot.pieces != 0:
                other_win = False

        if sb_constants.players_colors[self.name] == "black":
            if board.burned_black.pieces != 0:
                you_win = False
            elif board.burned_white.pieces != 0:
                other_win = False
        else:
            if board.burned_black.pieces != 0:
                other_win = False
            elif board.burned_white.pieces != 0:
                you_win = False

        if you_win:
            self.conn.send("WIN")
        elif other_win:
            self.conn.send("LOS")
        else:
            self.conn.send("NON")

    def run(self):
        global total_clients
        global father_going_to_close
        global threads
        global dice
        global board
        global turn

        while total_clients != 2:
            self.conn.send("GNS")
        print "got 2 clients", "tid", str(self.tid)
        self.conn.send("GMS")

        print "New Thread, New connection from : " + self.ip + ":" + str(self.port)
        self.conn.settimeout(None)

        print board
        if self.turn_is_yours():
            self.conn.send("STT~you")
        else:
            self.conn.send("STT~him")

        while True:
            # try:
                time.sleep(1)
                ######################################################################################
                if self.turn_is_yours():
                    data = self.conn.recv(1024)
                    temp_dice = self.get_tuple_from_msg(data)
                    dice = temp_dice
                    moves_count = 2
                    if temp_dice[0] == temp_dice[1]:
                        moves_count = 4
                        temp_dice.append(temp_dice[0])
                        temp_dice.append(temp_dice[1])
                    while moves_count > 0:
                        # can_move = self.check_entry(temp_dice)
                        # self.conn.send("CHE~" + str(can_move))
                        movement_data = self.conn.recv(1024)
                        if not self.check_entry(temp_dice):
                            self.conn.send("NOEN")
                            moves_count = 0
                        elif self.is_legal(movement_data, temp_dice):
                            self.change_board(movement_data)
                            self.conn.send(self.pickled_board())
                            moves_count -= 1
                        else:
                            self.conn.send("ERR")

                    self.change_turn()
                    time.sleep(3)
                    self.check_win()
                else:  # turn is  not yours
                    while dice is None:
                        self.conn.send("NRL")
                        time.sleep(1)
                    temp_dice = dice
                    print "temp dice", temp_dice
                    dice = None
                    print "dice", str(temp_dice[0]), str(temp_dice[1])
                    self.conn.send("RDR~%s~%s" % (str(temp_dice[0]), str(temp_dice[1])))
                    while not self.turn_is_yours():
                        time.sleep(1)
                        self.conn.send("WFM")
                    self.conn.send(self.pickled_board())
                    self.check_win()
                ######################################################################################
            # except socket.error as e:
            #     if e.errno == sb_constants.ECONNRESET:  # 'Connection reset by peer'
            #         print "Error %s - Seems Client Disconnect. try Accept new Client " % e.errno
            #         break
            #     elif e.errno == sb_constants.EWOULDBLOCK or str(e) == "timed out":  # if we use conn.settimeout(x)
            #         if father_going_to_close:
            #             print "Father Going To Die"
            #             self.conn.close()
            #             break
            #         print ",",
            #         continue
            #     else:
            #         print "Unhandled Socket error at recv. Server will exit %s " % e
            #         break
            # except Exception as general_err:
            #     print "General Error - ", general_err.args
            #     break
            # if data == "":
            #     print "\nGot empty data from recv.\nWill close this client socket\n"
            #     break
            # if self.end:
            #     break

        print "Client disconnected..."
        change_total_clients.acquire()
        total_clients -= 1
        change_total_clients.release()

        self.conn.close()


def main(ip, port):
    global total_clients
    global father_going_to_close

    # log_total_clients(total_clients)

    srv_sock = socket.socket()

    srv_sock.bind((ip, port))
    srv_sock.listen(2)


    tid = 0

    # srv_sock.settimeout(10)
    while True:
        conn, (ip, port) = srv_sock.accept()

        if total_clients < 2:
            print "tc", str(total_clients)
            total_clients += 1

            print "\nNEW CLIENT\n"
            tid += 1

            conn.send("OKE")
            new_thread = ClientThread(socket.gethostname(), port, conn, tid)

            new_thread.start()

            threads.append(new_thread)

        else:
            conn.send("ERR~00")
            conn.close()

    srv_sock.close()
    for t in threads:
        t.join()

if __name__ == "__main__":
    try:
        if len(argv) != 2:
            print "Usage: sb_server.py <port>"
            exit()
        else:
            main('0.0.0.0', int(argv[1]))
    except KeyboardInterrupt:
        print "\nGot ^C Main\n"
        father_going_to_close = True
