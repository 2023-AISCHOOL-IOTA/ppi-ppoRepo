import RPi.GPIO as GPIO
import time

MOTER1_PIN1 = 24
MOTER1_PIN2 = 23
MOTER2_PIN1 = 21
MOTER2_PIN2 = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup([MOTER1_PIN1, MOTER1_PIN2, MOTER2_PIN1, MOTER2_PIN2], GPIO.OUT)

motor_state = False  # 모터 상태를 추적하는 변수 (회전 중: True, 정지: False)

def command_one(command):
    global motor_state # 전역 변수 motor_state 사용
    if command == '1':
        if motor_state:  # 모터가 이미 회전 중인 경우
            GPIO.output([MOTER1_PIN1, MOTER1_PIN2, MOTER2_PIN1, MOTER2_PIN2], GPIO.LOW)  # 모터 정지
            motor_state = False
        else:  # 모터가 정지 상태인 경우
            GPIO.output(MOTER1_PIN1, GPIO.HIGH)  # 모터1 회전
            GPIO.output(MOTER2_PIN1, GPIO.HIGH)  # 모터2 회전
            motor_state = True  # 모터 상태를 회전 중으로 변경