import random
from asyncio import sleep

import websockets
import asyncio
import json


PORT = 7890
URL = "localhost"


def get_command_from_input(x: int, y: int) -> dict:
    return {"acceleration": y, "direction": x, "source": "CONTROLLER"}


def generate_command() -> dict:
    x = random.randint(-1, 1)
    y = random.randint(-1, 1)
    return get_command_from_input(x=x, y=y)


async def start_controlling():
    async with websockets.connect(f'ws://{URL}:{PORT}/controller') as websocket:
        await websocket.send("Autonomous Controller connected")
        while True:
            time_to_sleep = random.randint(2, 3)
            await sleep(time_to_sleep)
            command = generate_command()
            await websocket.send(json.dumps(command))


asyncio.run(start_controlling())
