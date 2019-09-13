import asyncio

SERVER_IP = '192.168.1.43'
SERVER_PORT = 9998

COMMANDS = ['dir', 'netstat -an']

class CmdClientProtocol(asyncio.Protocol):
    def data_received(self, data):
        print(data.decode(),end='')

    def connection_lost(self, exc):
        self._transport.close()


async def main():
    loop = asyncio.get_running_loop()

    transport, protocol = await loop.create_connection(
        CmdClientProtocol,
        SERVER_IP, SERVER_PORT)

    for command in COMMANDS:
        print('发送命令：', command)
        transport.write(command.encode())
        await asyncio.sleep(1)


asyncio.run(main())
