import asyncio
from email import message
import json
import websockets


PORT = 7890
URL = "localhost"

def handle_command(command: dict):
    if command["source"] != "CONTROLLER":
        print("Command not for me")
        return
    
    y = command["acceleration"]
    x = command["direction"]
    print(f'x:{x}   y:{y}')


async def main():
    async with websockets.connect(f'ws://{URL}:{PORT}') as websocket:
        await websocket.send("Racer connected")
        while True:
            message = await websocket.recv()
            try:
                command = json.loads(message)
                handle_command(command)
            except:
                print(message)
                pass


    await asyncio.Future() # run forever

asyncio.run(main())