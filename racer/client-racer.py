import asyncio
import json
from json import JSONDecodeError

import websockets

from racer.racer import Racer

PORT = 7890
URL = "moritzs-m1pro.local"


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
    while True:
        try:
            await connect_and_listen(racer_hardware)
        except RuntimeError as e:
            racer_hardware.stop()
            print(f'BREAK: {e}')
        except BaseException as e:
            racer_hardware.stop()
            print(f'BREAK: {e}')


async def connect_and_listen(racer_hardware):
    try:
        async with websockets.connect(f'ws://{URL}:{PORT}/racer') as websocket:
            await websocket.send("Racer connected")
            while True:
                message = await websocket.recv()
                await handle_incoming_message(message, racer_hardware)
    except ConnectionError as e:
        print(f'{message}: {e}')
        racer_hardware.stop()
        await asyncio.sleep(1)


async def handle_incoming_message(message, racer_hardware):
    try:
        command = json.loads(message)
        handle_command(command, racer_hardware)
    except JSONDecodeError as e:
        print(f'{message}: {e}')
        pass
    except BaseException as e:
        print(f'{message}: {e}')
        pass


asyncio.run(main())
