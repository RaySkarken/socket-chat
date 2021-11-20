import socket
import threading
import sys

from include import send_msg

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.0.202"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    send_msg(msg, client, HEADER, FORMAT)


def listen_to_server():
    while True:
        msg_len = int(client.recv(HEADER).decode(FORMAT))
        if msg_len:
            message = client.recv(msg_len).decode(FORMAT)
            print(f"[OurChan] {message}")


if __name__ == '__main__':
    print("to disconnect print \"!DISCONNECT\"")
    listen_thread = threading.Thread(
        target=listen_to_server, daemon=True)
    listen_thread.start()
    msg = input()
    while msg != DISCONNECT_MESSAGE:
        send(msg)
        msg = input()

    send(DISCONNECT_MESSAGE)
    sys.exit()
