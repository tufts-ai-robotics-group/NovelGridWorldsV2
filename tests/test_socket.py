import socket

##### server
s = socket.socket()
s.bind(('localhost', 2345))
s.listen()
s.setblocking(False)


c, addr = s.accept()

msg = ""
done = False
while not done:
    slice_msg = c.recv(1024, socket.MSG_PEEK)
    if b'\n' in slice_msg:
        index = slice_msg.find(b'\n')
        msg += c.recv(index).decode('unicode-escape')
        c.recv(1)
        done = True

#### client
client = socket.socket()
client.connect(('localhost', 2345))

client.send(b"12345\n")
