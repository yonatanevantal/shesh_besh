__author__ = 'yonatan'

import socket
import threading
import sb_constants
from sys import argv
from sb_graphics import Game

GAME = Game()
add_to_log = threading.Lock()

def get_logged_total_clients():
    with add_to_log:
        with open(sb_constants.LOG_FILE, 'rb+') as f:
            tc = f.read()
        return int(tc)


def main(ip, port):
    total_clients = get_logged_total_clients()
    if total_clients < sb_constants.NUM_CLIENTS:
        cln_sock = socket.socket()
        cln_sock.connect((ip, port))
        print "After connect"

        cln_sock.send("HLS")
        while True:
            try:
                data = cln_sock.recv(1024)
            except socket.error as e:
                if e.errno == sb_constants.EWOULDBLOCK or str(e) == "timed out":
                    continue
                else:
                    print "Unhandled Socket error at recv. Server will exit %s " % e
                    break

            except Exception as general_err:
                print "General Error - ", general_err.args
                break

            to_send = handle_received_data(data)

            GAME.handle_board()

    else:
        print "\nA match is in occurrence.\nPlease try again later.\n"


def get_msg_prefix(data):
    return str(data[0] + data[1] + data[2])


def handle_received_data(data):
    global GAME
    if get_msg_prefix(data) == "HLC":
        name = data.split('~')[1]
        GAME.board.me.name = name
        GAME.board.me.color = sb_constants.players_colors[name]
        to_send = ""

    return to_send

if __name__ == "__main__":
    if len(argv) != 3:
        print "Usage: sb_client.py <ip> <port>"
    else:
        main(argv[1], int(argv[2]))