import websockets
import asyncio


PORT = 7890
URL = "localhost"


async def echo(websocket):
    async for message in websocket:
        print(message)
        try:
            await websocket.send(message)
        except websockets.exceptions.ConnectionClosed:
            print("Client disconnected. Do cleanup")
            break


async def main():
    async with websockets.serve(echo, URL, PORT):
        await asyncio.Future() # run forever


asyncio.run(main())