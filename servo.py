from gpiozero import AngularServo
from time import sleep

pin = 17
servo = AngularServo(pin, initial_angle=0, min_angle=-15, max_angle=15)


def setup():
    print("setup")
    servo.angle = 0
    # servo.mid()
    print(servo.angle)


def update():
    print("update")
    steer_left()
    print(servo.angle)
    sleep(1)
    steer_right()
    print(servo.angle)
    sleep(1)
    center()
    print(servo.angle)
    sleep(3)


def steer_left():
    servo.angle = -10
    

def steer_right():
    servo.angle = 15


def center():
    servo.angle = 0

if __name__ == '__main__':
    setup()
    while True:
       update()

