from gpiozero import AngularServo
import RPi.GPIO as GPIO

SERVO_PIN = 17

ENGINE_PWMA1 = 20
ENGINE_PWMA2 = 21
ENGINE_D1 = 26


class Racer:
    __servo = AngularServo(SERVO_PIN, initial_angle=0, min_angle=-15, max_angle=15)

    def __init__(self) -> None:
        self.__setup_servo()
        self.__setup_engine()

    def __setup_servo(self):
        self.__servo.angle = 0

    def __setup_engine(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(ENGINE_PWMA1, GPIO.OUT)
        GPIO.setup(ENGINE_PWMA2, GPIO.OUT)
        GPIO.setup(ENGINE_D1, GPIO.OUT)
        GPIO.output(ENGINE_D1, 1)

    def steer_left(self):
        self.__servo.angle = -10

    def steer_right(self):
        self.__servo.angle = 15

    def center(self):
        self.__servo.angle = 0

    def __set_motor(self, A1, A2):  # A1 forward | A2 reverse
        GPIO.output(ENGINE_PWMA1, A1)
        GPIO.output(ENGINE_PWMA2, A2)

    def forward(self):
        self.__set_motor(1, 0)

    def stop(self):
        self.__set_motor(0, 0)

    def reverse(self):
        self.__set_motor(0, 1)
