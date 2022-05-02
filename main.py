from gpiozero import Servo
from time import sleep

pin = 18
servo = Servo(pin)


def setup():
    print("setup")


def update():
    print("update")
    servo.min()
    sleep(1)
    servo.mid()
    sleep(1)
    servo.max()
    sleep(1)


if __name__ == '__main__':
    setup()
    while True:
        update()
