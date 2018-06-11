import socket
import threading
import sb_constants
from sys import argv

LOG = True
ply_num = 2
total_clients = 0
father_going_to_close = False
__author__ = 'yonatan'

# add locks as needed
add_to_log = threading.Lock()
get_player_num = threading.Lock()
change_total_clients = threading.Lock()


def log_total_clients(num):
    with add_to_log:
        with open(sb_constants.LOG_FILE, 'w'):
            pass
        with open(sb_constants.LOG_FILE, 'w') as f:
            f.write(str(num))


class ClientThread(threading.Thread):
    def __init__(self, ip, port, conn, tid):
        global ply_num
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn
        self.tid = tid
        self.name = "player" + str(ply_num % 2 + 1)
        ply_num += 1

    def handle_received_data(self, data):
        if data == "HLS":
            to_send = "HLC~" + self.name
            to_close = False

        return to_close, to_send

    def run(self):
        global total_clients
        global father_going_to_close

        change_total_clients.acquire()
        total_clients += 1
        log_total_clients(total_clients)
        print "server", total_clients
        change_total_clients.release()

        print "New Thread, New connection from : " + self.ip + ":" + str(self.port)
        self.conn.settimeout(None)
        while True:
            try:
                data = self.conn.recv(1024)
            except socket.error as e:
                if e.errno == sb_constants.ECONNRESET:  # 'Connection reset by peer'
                    print "Error %s - Seems Client Disconnect. try Accept new Client " % e.errno
                    break
                elif e.errno == sb_constants.EWOULDBLOCK or str(e) == "timed out":  # if we use conn.settimeout(x)
                    if father_going_to_close:
                        print "Father Going To Die"
                        self.conn.close()
                        break
                    print ",",
                    continue
                else:
                    print "Unhandled Socket error at recv. Server will exit %s " % e
                    break
            except Exception as general_err:
                print "General Error - ", general_err.args
                break
            if data == "":
                print "\nGot empty data from recv.\nWill close this client socket\n"
                break

            print str(self.tid) + ": Received<<< " + data
            to_close, to_send = self.handle_received_data(data)

            self.conn.send(to_send)
            print str(self.tid) + ": Sent>>> " + to_send

            if to_close:
                break

        print "Client disconnected..."
        change_total_clients.acquire()
        total_clients -= 1
        log_total_clients(total_clients)
        change_total_clients.release()

        self.conn.close()


def main(ip, port):
    global total_clients
    global father_going_to_close

    log_total_clients(total_clients)

    srv_sock = socket.socket()

    srv_sock.bind((ip, port))
    srv_sock.listen(2)

    threads = []
    tid = 0

    # srv_sock.settimeout(10)
    while True:
        with change_total_clients:
            enter = total_clients < sb_constants.NUM_CLIENTS

        if enter:
            conn, (ip, port) = srv_sock.accept()

            print "\nNEW CLIENT\n"
            tid += 1

            new_thread = ClientThread(socket.gethostname(), port, conn, tid)

            new_thread.start()

            threads.append(new_thread)
            # add error handling

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
