import asyncio
import os

SERVER_IP = '0.0.0.0'
SERVER_PORT = 9998

class CmdServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self._transport = transport

    def data_received(self, data):
        command = data.decode()
        print('Command received: {!r}'.format(command))

        command = command.split('\n')[0]

        if command=='exit':
            print('Exit receive, close the socket')
            self._transport.close()

        result = os.popen(command)
        self._transport.write(result.read().encode())

    def connection_lost(self, exc):
        print('Close the client socket')
        self._transport.close()


async def main():
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        CmdServerProtocol,
        SERVER_IP, SERVER_PORT)

    async with server:
        await server.serve_forever()


asyncio.run(main())
