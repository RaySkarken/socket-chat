import socket
import threading
import time

from include import User, send_msg

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTIONS] {addr} connected.")
    user = User(conn, addr)
    connected = True
    while connected:
        if user.is_free():
            send_msg("Wait until someone connects to your room", conn, HEADER,
                     FORMAT)

        msg_length_b = conn.recv(HEADER)
        if msg_length_b:
            msg_length = int(msg_length_b.decode(FORMAT))
            msg_b = conn.recv(msg_length)
            msg = msg_b.decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                send_msg("Disconnected from the server.", conn, HEADER, FORMAT)
                if not user.is_free():
                    user.send('Your interlocutor has left the chat.', HEADER,
                              FORMAT)
                user.leave()
            elif not user.is_free():
                user.send_b(msg_length_b, msg_b)
            else:
                send_msg("Chat room is empty. Wait until someone connects to "
                         "your room", conn, HEADER, FORMAT)

    conn.close()


def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


if __name__ == '__main__':
    print("[STARTING] The server is starting...")
    print(ADDR)
    start()
