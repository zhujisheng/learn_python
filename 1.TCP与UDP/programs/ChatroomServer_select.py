'''
本程序实现聊天室服务——当多个客户端连接后，任何一个客户端发送的数据，都能被其它的客户端收到。
'''

'''
一些变量值的含义：
server:   socket类型，监听9999端口的服务器socket
inputs:   list类型，包含所有的socket(server以及每个客户端连接)
outputs： list类型，当前需要给这些客户端连接发送数据（有数据发送时，加入outputs；没有数据时，从outputs从删除
message_queues: 字典类型，每个客户端连接对应其中一个元素。key是客户端连接的socket，value是一个队列，其中包含需要传输给这个客户端的信息。
'''

import select
import socket
import queue

server_address = ( '0.0.0.0', 9999 )

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(server_address)
server.listen()

inputs = [server]
outputs = []

# message_queues[socket1]=队列A，意味着要向socket1发送队列A中的每条信息
message_queues = {}

while(True):
    readable , writable , exceptional = select.select(inputs, outputs, inputs)

    for available_sock in readable :
        if available_sock is server:
            # 监听socket可读，意味着有新的连接
            connection, client_address = server.accept()
            print( "新的连接：(%s:%s)"%client_address )
            inputs.append(connection)
            message_queues[connection] = queue.Queue()
        else:
            # 建立连接的socket可读，意味着有新的数据需要接收
            data = available_sock.recv(1024)
            if data :
                # 接收消息并处理
                message = "(%s:%s): "%available_sock.getpeername() + data.decode()
                print(message)
                # 消息需要发送给除自己与server之外的所有客户端连接socket
                # 消息放入socket对应的队列中，socket放入select的wlist
                for sock in message_queues.keys():
                    if sock is not available_sock:
                        message_queues[sock].put(message)
                        if sock not in outputs:
                            outputs.append(sock)
            else:
                #  收到数据为空则关闭连接
                print ("关闭连接：(%s:%s)"%available_sock.getpeername())
                inputs.remove(available_sock)
                if available_sock in writable:
                    writable.remove(available_sock)
                if available_sock in outputs:
                    outputs.remove(available_sock)
                available_sock.close()
                del message_queues[available_sock]

    for available_sock in writable:
        try:
            msg = message_queues[available_sock].get_nowait()
        except queue.Empty:
            outputs.remove(available_sock)
        else:
            available_sock.send(msg.encode())
     
    for available_sock in exceptional:
        print ( "连接关闭：(%s:%s)"%available_sock.getpeername())
        inputs.remove(available_sock)
        if available_sock in outputs:
            outputs.remove(available_sock)
        available_sock.close()
        del message_queues[available_sock]
