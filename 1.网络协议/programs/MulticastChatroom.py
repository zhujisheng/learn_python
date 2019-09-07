'''
本程序基于组播实现聊天室功能——任一程序输入的内容，会在其它程序中显示。
两个线程，主线程接受终端输入，并发送给组播地址；另一个线程接受组播消息并显示在屏幕上。
'''

import socket
import os
import struct
import threading

port = 9999
multicast_group = "224.99.99.99"

# 监听收到的消息并显示
def listen_print():
    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recv_sock.bind(("0.0.0.0", port))

    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    recv_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        # 接收数据:
        msg, addr = recv_sock.recvfrom(1024)
        print('(%s:%s): '%addr, msg.decode())

# 接收键盘输入，发送到组播地址
def send_message():
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        message = input()
        send_sock.sendto(message.encode('utf-8'), (multicast_group, port))
        if message=='exit':
            os._exit(0)


t = threading.Thread(target=listen_print)
t.start()
send_message()
