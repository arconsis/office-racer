import os
from pynput import keyboard


def on_press(key):    
    try:
        keys_pressed.add(key.char)
    except:
        pass
    
    
def on_release(key):
    try:
        keys_pressed.remove(key.char)
    except:
        pass
    

def get_command_from_input(x: int, y: int) -> str:
    acceleration = ''
    if y > 0:
        acceleration = "FORWARD"
    elif y < 0:
        acceleration = "BACKWARD"
    else:
        acceleration = "STOP"
    
    direction = ''
    if x > 0:
        direction = "LEFT"
    elif x < 0:
        direction = "RIGHT"
    else:
        direction = "STRAIGHT"
    
    return f'{acceleration}-{direction}'

def get_command_from_pressed_keys() -> str:
    x = 0
    y = 0
    if 'a' in keys_pressed:
        x+=1

    if 'd' in keys_pressed:
        x-=1
    
    if 'w' in keys_pressed:
        y+=1

    if 's' in keys_pressed:
        y-=1

    return get_command_from_input(x=x, y=y)


listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

keys_pressed = set()
is_running = True
last_command = ""
os.system('cls' if os.name == 'nt' else 'clear')
while is_running:
    if 'q' in keys_pressed:
        is_running = False
    command = get_command_from_pressed_keys()
    if command != last_command:
        last_command = command
        # clear screen and print last command
        os.system('cls' if os.name == 'nt' else 'clear')
        print(last_command)


    