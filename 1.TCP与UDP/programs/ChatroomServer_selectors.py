'''
本程序实现聊天室服务——当多个客户端连接后，任何一个客户端发送的数据，都能被其它的客户端收到。

一些变量值的含义：
server:   socket类型，监听9999端口的服务器socket
message_queues: 字典类型，每个客户端连接对应其中一个元素。key是客户端连接的socket，value是一个队列，其中包含需要传输给这个客户端的信息。
'''

import socket
import queue
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

sel = DefaultSelector()

def listen_accept(available_sock, ev):
    conn, addr = available_sock.accept()
    print( "新的连接：(%s:%s)"%addr )
    sel.register(conn, EVENT_READ, data=recv_send)
    message_queues[conn] = queue.Queue()

def recv_send(available_sock, ev):
    if ev&EVENT_READ:
        data = available_sock.recv(1024)
        if data :
            # 接收消息并处理
            message = "(%s:%s): "%available_sock.getpeername() + data.decode()
            print(message)
            # 消息需要发送给除自己之外的所有客户端连接socket
            for sock in message_queues.keys():
                if sock is not available_sock:
                    message_queues[sock].put(message)
                    sel.modify( sock, EVENT_READ|EVENT_WRITE, data=recv_send )

        else:
            #  收到数据为空则关闭连接
            print ("关闭连接：(%s:%s)"%available_sock.getpeername())
            sel.unregister(available_sock)
            available_sock.close()
            del message_queues[available_sock]

    if ev&EVENT_WRITE:
        try:
            msg = message_queues[available_sock].get_nowait()
        except queue.Empty:
            sel.modify( available_sock, EVENT_READ, data=recv_send )
        else:
            available_sock.send(msg.encode())


server_address = ( '0.0.0.0', 9999 )
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(server_address)
server.listen()
sel.register(server, EVENT_READ, data=listen_accept)

# message_queues[socket1]=队列A，意味着要向socket1发送队列A中的每条信息
message_queues = {}

while True:
    events = sel.select()
    for key, ev in events:
        key.data(key.fileobj, ev)