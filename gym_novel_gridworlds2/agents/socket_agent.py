from .keyboard_agent import KeyboardAgent
import socket

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
        super().__init__(**kwargs)
    
    def is_ready(self):
        if self.conn is not None:
            return True
        else:
            try:
                self.conn, self.conn_addr = self.socket.accept()
                print(f"agent {self.name}: socket is ready.")
            except BlockingIOError:
                print(f"agent {self.name}: socket not ready yet.")
                pass
    
    def _recv_msg(self) -> str:
        msg = ""
        done = False
        while not done:
            slice_msg = self.conn.recv(1024, socket.MSG_PEEK)
            if b'\n' in slice_msg:
                index = slice_msg.find(b'\n')
                msg += self.conn.recv(index).decode('unicode-escape')
                self.conn.recv(1)
                done = True
        return msg

    def _send_msg(self, msg: str):
        data = msg.encode('unicode-escape')
        while data:
            sent = self.conn.send(data)
            data = data[sent:]
        return True
    
    def policy(self, observation):
        self._send_msg(f">>>>>>>>> keyboard agent: Agent {self.name} can do these actions:")
        action_names = self.action_set.get_action_names()
        self._send_msg(">>>>>>>>>> ", ', '.join([f"{index}: {name}" for (index, name) in enumerate(action_names)]))
        action = self._recv_msg()
        return int(action)
    
    def __del__(self):
        if self.conn is not None:
            self.conn.close()
        self.socket.close()
