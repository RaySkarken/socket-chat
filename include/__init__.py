class User:
    free_users = []
    num_users = 0
    max_users = 100

    def __init__(self, socket, addr):
        self.socket = socket
        self.addr = addr
        self.interlocutor = None
        User.num_users += 1
        self.release()

    def leave(self):
        if self.interlocutor:
            self.interlocutor.interlocutor = None
            self.interlocutor.release()
            self.interlocutor = None
        User.num_users -= 1
        del self

    def release(self):
        if User.free_users and User.num_users <= User.max_users:
            self.interlocutor = User.free_users.pop(0)
            self.interlocutor.interlocutor = self
            send_msg("Someone connected to your room, so now you can chat!",
                     self.socket, 64, 'utf-8')
            send_msg("Someone connected to your room, so now you can chat!",
                     self.interlocutor.socket, 64, 'utf-8')
        else:
            User.free_users.append(self)

    def send_b(self, msg_len_b, msg_b):
        self.interlocutor.socket.send(msg_len_b)
        self.interlocutor.socket.send(msg_b)

    def send(self, msg, header, formt):
        send_msg(msg, self.interlocutor.socket, header, formt)

    def is_free(self):
        return self in User.free_users


def send_msg(msg, sockt, header, formt):
    message = msg.encode(formt)
    msg_length = len(message)
    send_length = str(msg_length).encode(formt)
    send_length += b' ' * (header - len(send_length))
    sockt.send(send_length)
    sockt.send(message)
