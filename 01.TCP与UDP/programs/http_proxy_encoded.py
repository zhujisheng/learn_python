#!/usr/bin/env python3

import socket
import threading
import re
from selectors import DefaultSelector, EVENT_READ

# Proxy开放的端口号
LOCAL_PORT = 7088

# 一些Proxy返回的状态码
STATUS_200 = b'HTTP/1.1 200 Connection established\nProxy-agent: Python_Proxy_1.0\n\n'
STATUS_400 = b'HTTP/1.1 400 Bad Request\nProxy-agent: Python_Proxy_1.0\n\n'
STATUS_502 = b'HTTP/1.1 502 Bad Gateway\nProxy-agent: Python_Proxy_1.0\n\n'


def xor_encode( bstring ):
    """一个简单编码：两次编码后与原值相同"""
    MASK = 0x55
    ret = bytearray( bstring )
    for i in range(len(ret)):
        ret[i] ^= MASK
    return ret


def proxy_process_encoded( sock1, sock2 ):
    """在两个sockek之间转发数据：任何一个收到的，编码后转发到另一个"""
    from selectors import DefaultSelector, EVENT_READ
    sel = DefaultSelector()
    sel.register(sock1, EVENT_READ)
    sel.register(sock2, EVENT_READ)

    while True:
        events = sel.select()
        for (key,ev) in events:
            try:
                data_in = key.fileobj.recv(8192)
            except ConnectionResetError as e:
                print(key.fileobj, "\nreset receive!")
                sock1.close()
                sock2.close()
                return
            if data_in:
                if key.fileobj==sock1:
                    sock2.send(xor_encode(data_in))
                else:
                    sock1.send(xor_encode(data_in))
            else:
                sock1.close()
                sock2.close()
                return

def http_proxy_encoded(sock_in, addr):
    """新的代理请求连接时，进行相关处理"""

    print("新的连接: %s:%s..." % addr)

    data = xor_encode(sock_in.recv(1024))

    # 非HTTP代理
    if data.startswith(b'CONNECT '):
        is_http = False
        remote = data.split()[1].decode().split(':')
        remote_addr = remote[0]
        remote_port = int(remote[1])

    # HTTP代理
    else:
        match = re.match(r'^(POST |GET |OPTIONS |HEAD |PUT )http://(.+?)(?::(\d+)){0,1}(/(?:.|\t|\n)*)$', data.decode())
        if not match:
            sock_in.send( xor_encode(STATUS_400) )
            sock_in.close()
            return
        is_http = True
        remote_addr = match.group(2).encode()
        remote_port = int(match.group(3)) if match.group(3) else 80
        request_data = match.group(1).encode() + match.group(4).encode()

    # 建立远程连接
    sock_remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_remote.settimeout(15)
    try:
        sock_remote.connect((remote_addr, remote_port))
        if is_http:
            sock_remote.send(request_data)
    except Exception as e:
        print(e)
        print( "Error when connect to", (remote_addr, remote_port) )
        
        sock_in.send( xor_encode(STATUS_502) )
        sock_in.close()
        return
    sock_remote.settimeout(0)

    if not is_http:
        sock_in.send( xor_encode(STATUS_200) )

    proxy_process_encoded( sock_in, sock_remote )


def start_server():
    """主服务函数"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", LOCAL_PORT))
    s.listen()
    print("等待客户端连接...")

    while True:
        sock, addr = s.accept()
        t = threading.Thread(target=http_proxy_encoded, args=(sock, addr))
        t.start()


if __name__ == "__main__":
    start_server()