import websockets
import asyncio


PORT = 7890
URL = "localhost"


async def start_racer():
    try:
        async with websockets.connect(f'ws://{URL}:{PORT}/racer') as websocket:
            await websocket.send("Racer connected")
            while True:
                message = await websocket.recv()
                print(message)
    except ConnectionError as e:
        print(f'{message}: {e}')
        await asyncio.sleep(1)

asyncio.run(start_racer())
