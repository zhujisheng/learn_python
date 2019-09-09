'''
本程序实现聊天室服务——当多个客户端连接后，任何一个客户端发送的数据，都能被其它的客户端收到。

一些变量值的含义：
outputs: 所有需要发送消息的StreamWriter。
'''

import asyncio

outputs = []

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    outputs.append(writer)
    print( "新的连接：(%s:%s)"%addr )

    while True:
        data = await reader.read(1024)
        if data:
            message = "(%s:%s): "%writer.get_extra_info('peername') + data.decode()
            print(message)

            for w in outputs:
                if w is not writer:
                    w.write(message.encode())
                    await writer.drain()
        else:
            print ("关闭连接：(%s:%s)"%writer.get_extra_info('peername'))
            outputs.remove(writer)
            writer.close()
            await writer.wait_closed()
            break

async def main():
    server = await asyncio.start_server( handle_client, '0.0.0.0', 9999)

    async with server:
        await server.serve_forever()

asyncio.run(main())
