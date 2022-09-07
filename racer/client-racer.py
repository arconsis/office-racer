import asyncio
import json
import websockets

from racer.racer import Racer

PORT = 7890
URL = "192.168.2.222"


def handle_command(command: dict, racer: Racer):
    if command["source"] != "CONTROLLER":
        print("Command not for me")
        return

    y = command["acceleration"]
    x = command["direction"]

    if x < 0:
        racer.steer_left()
    elif x > 0:
        racer.steer_right()
    else:
        racer.center()

    if y < 0:
        racer.reverse()
    elif y > 0:
        racer.forward()
    else:
        racer.stop()


async def main():
    racer_hardware = Racer()
    async with websockets.connect(f'ws://{URL}:{PORT}/racer') as websocket:
        await websocket.send("Racer connected")
        while True:
            try:
                message = await websocket.recv()
                command = json.loads(message)
                handle_command(command, racer_hardware)
            except:
                racer_hardware.stop()
                pass

    await asyncio.Future()  # run forever


asyncio.run(main())
