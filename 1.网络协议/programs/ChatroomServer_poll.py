'''
本程序实现聊天室服务——当多个客户端连接后，任何一个客户端发送的数据，都能被其它的客户端收到。
'''

'''
一些变量值的含义：
server:   socket类型，监听9999端口的服务器socket
message_queues: 字典类型，每个客户端连接对应其中一个元素。key是客户端连接的socket，value是一个队列，其中包含需要传输给这个客户端的信息。
fd_to_socket:  字典类型，key包含每一个socket（server以及每一个客户端连接）的file_no，value是对应的socket
'''

import select
import socket
import queue

server_address = ( '0.0.0.0', 9999 )

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(server_address)
server.listen()

# message_queues[socket1]=队列A，意味着要向socket1发送队列A中的每条信息
message_queues = {}

READ_ONLY = select.EPOLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR
READ_WRITE = READ_ONLY|select.POLLOUT
poller = select.poll()
poller.register( server, READ_ONLY )

fd_to_socket = {server.fileno():server}

while(True):
    events = poller.poll()
    for fd, flag in events:
        available_sock = fd_to_socket[fd]
        if flag & (select.POLLIN | select.POLLPRI):
            if available_sock is server:
                # server有新的数据可读，意味着有新的连接
                connection , client_address = available_sock.accept()
                print( "新的连接：(%s:%s)"%client_address )
                fd_to_socket[connection.fileno()] = connection
                poller.register( connection, READ_ONLY )
                message_queues[connection] = queue.Queue()
            else:
                # 非seve的socket可读，意味着从客户端有新的数据到达
                data = available_sock.recv(1024)
                if data :
                    # 接收消息并处理
                    message = "(%s:%s): "%available_sock.getpeername() + data.decode()
                    print(message)
                    # 消息需要发送给除自己之外的所有客户端连接socket
                    for sock in message_queues.keys():
                        if sock is not available_sock:
                            message_queues[sock].put(message)
                            poller.modify( sock, READ_WRITE )

                else:
                    #  收到数据为空则关闭连接
                    print ("关闭连接：(%s:%s)"%available_sock.getpeername())
                    poller.unregister(available_sock)
                    available_sock.close()
                    del message_queues[available_sock]
                    del fd_to_socket[fd]

        elif flag & select.POLLOUT:
            # 当消息可以发送给对应的socket时
            try:
                msg = message_queues[available_sock].get_nowait()
            except queue.Empty:
                poller.modify( available_sock, READ_ONLY )
            else:
                available_sock.send(msg.encode())

        elif flag & (select.POLLHUP|select.POLLERR):
            # 客户端关闭连接或者发生错误
            print ( "连接关闭：(%s:%s)"%available_sock.getpeername())
            poller.unregister(available_sock)
            available_sock.close()
            del message_queues[available_sock]
            del fd_to_socket[fd]