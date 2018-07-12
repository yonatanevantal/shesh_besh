__author__ = 'yonatan'

import time
import socket
import pickle
import pygame
import threading
import sb_constants
from sys import argv
from sb_graphics import *
from states import State

game = Game()
add_to_log = threading.Lock()
# board = GameBoard()
font = None
waiting_text = None


def load_start_screen():
    global game
    global font
    global waiting_text

    game.init_window()
    game.display.blit(game.start_menu, game.start_menu.get_rect())

    font = pygame.font.SysFont("comicsansms", 36)
    waiting_text = font.render("not your turn", True, (0, 0, 0))

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        if game.play_button():
            done = True
        elif game.instructions_button(pygame.mouse):
            game.open_instructions()

        pygame.display.flip()


def check_permission(cln_sock):
    check = cln_sock.recv(1024)
    print check
    if check.split('~')[0] == 'ERR' and check.split('~')[1] == '00':
        print "A match is in occurrence.\nPlease try again later.\n"
        cln_sock.close()
        exit()

    game.display.blit(game.waiting_screen, (0, 0))
    pygame.display.flip()


def check_participants(cln_sock):
    recv = cln_sock.recv(3)
    print recv
    while recv != "GMS":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        recv = cln_sock.recv(3)

    # print "!!!!!!!!!!!!!!!!!!"

    game.display.blit(game.background, (0, 0))
    pygame.display.flip()


def roll_dice(events):
    game.dice[0].roll_up()
    game.dice[1].roll_down()


def do_events():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    return events


def get_win(sock):
    sock.send("GEW")
    winner_data = sock.recv(3)
    if winner_data == "WIN":
        print "You WIN!"
        return True
    elif winner_data == "LOS":
        print "You LOSE"
        return True
    else:
        return False


def get_move():
    src = -1
    while True:
        events = do_events()
        clicked_slot, slot_id = game.get_clicked_slot(events)
        if clicked_slot is not None and src != slot_id:
            if src != -1:
                dst = slot_id
                return src, dst
            else:
                press_state = font.render("to", True, (0, 0, 0))
                game.display.blit(press_state, (0, 500))
                src = slot_id
                pygame.display.flip()


def main(ip, port):

    load_start_screen()

    cln_sock = socket.socket()
    cln_sock.connect((ip, port))
    print "After connect"

    check_permission(cln_sock)
    check_participants(cln_sock)

    button_pressed = False

    game.board.initialize_board()
    game.draw_slots()

    turn = cln_sock.recv(1024).split("~")[1]
    if turn == "you":
        state = State.rolling_dice
    else:
        state = State.waiting
    while True:
        # try:
                        #################################################################
            if state == State.rolling_dice:
                events = do_events()
                game.update_screen()

                if not button_pressed:
                    game.roll_button.show()
                if game.roll_button.is_pressed(events) and not button_pressed:
                    button_pressed = True
                    roll_dice(events)

                game.dice[0].show()
                game.dice[1].show()
                # pygame.draw.rect(game.display, (0, 0, 0), [game.board.burned_white.button.x, game.board.burned_white.button.y, game.board.burned_white.button.width, game.board.burned_white.button.height])
                # pygame.draw.rect(game.display, (0, 0, 0), [game.board.slots[1].button.x, game.board.slots[1].button.y, game.board.slots[1].button.width, game.board.slots[1].button.height])

                if game.dice[0].not_rolling() and button_pressed:
                    state = State.playing
                    cln_sock.send("RLD~%s~%s" % (str(game.dice[0].num), str(game.dice[1].num)))

            elif state == State.playing:    #############################################
                do_events()
                moves_count = 2
                if game.dice[0].num == game.dice[1].num:
                    moves_count = 4
                while moves_count > 0:
                    game.dice[0].show()
                    game.dice[1].show()
                    pygame.display.flip()
                    time.sleep(1)

                    # entry = bool(cln_sock.recv(1024).split("~")[1])
                    # if not entry:
                    #     moves_count = 0
                    #     cln_sock.send("GOTTYA")

                    choice = get_move()
                    choice = "MOV~%s~%s" % (str(choice[0]), str(choice[1]))
                    cln_sock.send(choice)

                    recv = cln_sock.recv(40000)
                    if recv == "NOEN":
                        moves_count = 0
                        illegal = font.render("DO NOT\nHAVE MOVES", True, (255, 0, 0))
                        game.display.blit(illegal, (500, 400))
                        pygame.display.flip()
                        time.sleep(0.5)

                    elif recv == "ERR":
                        print "Illegal move"
                        illegal = font.render("illegal move", True, (255, 0, 0))
                        game.display.blit(illegal, (500, 400))
                        pygame.display.flip()
                        time.sleep(0.5)
                    else:
                        print "success movement", recv[-9:]
                        print "success movement", recv[:9]

                        temp_board = pickle.loads(recv)

                        game.board = temp_board
                        moves_count -= 1

                    game.update_screen()
                    pygame.display.flip()

                state = State.waiting

                print 1

                if get_win(cln_sock):
                    break
                game.reset_dice()

            elif state == State.waiting:    ##############################################
                events = do_events()
                game.update_screen()
                game.display.blit(waiting_text, (500, 400))
                dice_result = cln_sock.recv(20)
                print 2
                if dice_result == "NRL":
                    pygame.display.flip()
                    continue
                dice_result = dice_result.split("~")[1:3]
                print dice_result
                roll_dice(events)

                while not game.dice[0].not_rolling():
                    game.update_screen()
                    game.display.blit(waiting_text, (500, 400))
                    game.dice[0].show()
                    game.dice[1].show()
                    pygame.display.flip()

                game.dice[0].set_num(int(dice_result[0]))
                game.dice[1].set_num(int(dice_result[1]))

                state = State.got_dice
            else:
                do_events()
                game.update_screen()
                game.display.blit(waiting_text, (500, 400))
                game.dice[0].show()
                game.dice[1].show()
                pygame.display.flip()
                board_data = cln_sock.recv(40000)
                if board_data == "WFM":
                    continue

                board_data = pickle.loads(board_data)
                game.board = board_data
                button_pressed = False
                game.reset_dice()
                state = State.rolling_dice

                if get_win(cln_sock):
                    break
            pygame.display.flip()
            ###################################################################
        # except socket.error as e:
        #     if e.errno == sb_constants.EWOULDBLOCK or str(e) == "timed out":
        #         continue
        #     else:
        #         print "Unhandled Socket error at recv. Server will exit %s " % e
        #         break
        #
        # except Exception as general_err:
        #     print "General Error - ", general_err.args
        #     break


if __name__ == "__main__":
    if len(argv) != 3:
        print "Usage: sb_client.py <ip> <port>"
    else:
        main(argv[1], int(argv[2]))