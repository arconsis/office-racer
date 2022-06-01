import RPi.GPIO as GPIO
from time import sleep


PWMA1 = 20 
PWMA2 = 21
D1 = 26 

def setup():
    print("setup")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(PWMA1,GPIO.OUT)
    GPIO.setup(PWMA2,GPIO.OUT)
    GPIO.setup(D1,GPIO.OUT)
    GPIO.output(D1, 1)
    # p1 = GPIO.PWM(D1, 500)
    # p1.start(50)

def	set_motor(A1,A2): # A1 forward | A2 reverse
	GPIO.output(PWMA1,A1)
	GPIO.output(PWMA2,A2)

def forward():
    set_motor(1,0)

def stop():
    set_motor(0,0)

def reverse():
    set_motor(0,1)



def update():
    print("update")
    sleep(1)
    forward()
    print("forward")
    sleep(1)
    stop()
    print("stop")
    sleep(1)
    reverse()
    print("reverse")
    sleep(1)
    stop()
    print("stop")

if __name__ == '__main__':
    setup()
    while True:
       update()