import time
from .keyboard_agent import KeyboardAgent
import socket, struct # socket

class SocketManualAgent(KeyboardAgent):
    """
    A simple agent that accepts commands from the internet and sends output back
    """
    def __init__(self, socket_host, socket_port, **kwargs):
        self.conn = None
        self.conn_addr = None
        self.socket = socket.socket()
        self.socket.bind((socket_host, socket_port))
        self.socket.listen(5)
        self.socket.setblocking(False)
        self.printed_await_message = False
        super().__init__(**kwargs)
    
    def is_ready(self):
        if self.conn is not None:
            return True
        else:
            try:
                self.conn, self.conn_addr = self.socket.accept()
                print(f"agent {self.id}: socket is ready.")
                return True
            except BlockingIOError:
                # print(f"agent {self.name}: socket not ready yet.")
                return False
    
    def _wait_for_ready(self):
        while not self.is_ready():
            if not self.printed_await_message:
                print(f"agent {self.id}: Waiting for socket agent to be ready...")
                self.printed_await_message = True
            time.sleep(2)

    def _recv_msg(self) -> str:
        self._wait_for_ready()

        msg = ""
        done = False
        while not done:
            try:
                slice_msg = self.conn.recv(1024, socket.MSG_PEEK)
                if b'\n' in slice_msg:
                    index = slice_msg.find(b'\n')
                    msg += self.conn.recv(index).decode('utf-8')
                    self.conn.recv(1)
                    done = True
            except BlockingIOError:
                pass
        return msg

    def _send_msg(self, msg: str):
        self._wait_for_ready()

        data = (msg + '\n').encode('utf-8')
        while data:
            sent = self.conn.send(data)
            data = data[sent:]
        return True
    
    def policy(self, observation):
        action = ""
        while not action.isdecimal():
            self._send_msg(f">>>>>>>>> keyboard agent: Agent {self.id} can do these actions:")
            action_names = self.action_set.get_action_names()
            self._send_msg(">>>>>>>>>> " + ', '.join([f"{index}: {name}" for (index, name) in enumerate(action_names)]))
            action = self._recv_msg()
        return int(action)
    
    def __del__(self):
        if self.conn is not None:
            self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
            self.conn.close()
        self.socket.close()
