import websockets
import asyncio
import json
from pynput import keyboard

PORT = 7890
URL = "localhost"

keys_pressed = set()

def on_press_key(key):
    try:
        keys_pressed.add(key.char)
    except:
        print(f'Could not add key: {key.char}')

def on_release_key(key):
    try:
        keys_pressed.remove(key.char)
    except:
        print(f'Could not remove key: {key.char}')

def get_command_from_pressed_keys() -> dict:
    x = 0
    y = 0

    if 'a' in keys_pressed:
        x-=1

    if 'd'in keys_pressed:
        x+=1

    if 'w' in keys_pressed:
        y+=1

    if 's'in keys_pressed:
        y-=1

    return get_command_from_input(x=x, y=y)



def get_command_from_input(x: int, y: int) -> dict:
    controller_dict = {}
    controller_dict["acceleration"] = y
    controller_dict["direction"] = x
    controller_dict["source"] = "CONTROLLER"

    return controller_dict
    
    

async def start_controlling():
    listener = keyboard.Listener(
        on_press=on_press_key,
        on_release=on_release_key)
    listener.start()

    last_command = {}

    is_running = True

    async with websockets.connect(f'ws://{URL}:{PORT}/controller') as websocket:
        await websocket.send("Controller connected")
        while is_running:
            if 'q' in keys_pressed:
                is_running = False
            
            command = get_command_from_pressed_keys()
            if command != last_command:
                last_command = command
                await websocket.send(json.dumps(last_command))


asyncio.run(start_controlling())
