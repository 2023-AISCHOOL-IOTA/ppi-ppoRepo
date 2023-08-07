import RPi.GPIO as GPIO
import time

LED_PIN = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup([LED_PIN], GPIO.OUT)  # 이 부분은 led_pin이 아닌 LED_PIN이어야 합니다.

led_state = False

def command_two(command):
    global led_state  # 전역 변수 led_state 사용
    if led_state:  # LED가 이미 켜져 있는 경우
        GPIO.output(LED_PIN, GPIO.LOW)  # LED 끄기
    else:  # LED가 꺼져 있는 경우
        GPIO.output(LED_PIN, GPIO.HIGH)  # LED 켜기

    led_state = not led_state  # LED 상태 반전