import RPi.GPIO as GPIO
import time

# L293D 핀 설정
motor1_input1_pin = 24  # 모터1의 IN1 핀 번호
motor1_input2_pin = 23  # 모터1의 IN2 핀 번호

motor2_input1_pin = 21  # 모터2의 IN1 핀 번호
motor2_input2_pin = 20  # 모터2의 IN2 핀 번호

# LED 핀 설정
led_pin = 25  # LED의 핀 번호

# 버튼 핀 설정
button1_pin = 18  # 버튼1의 핀 번호
button2_pin = 17  # 버튼2의 핀 번호

# GPIO 핀 번호 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup([motor1_input1_pin, motor1_input2_pin, motor2_input1_pin, motor2_input2_pin, led_pin], GPIO.OUT)
GPIO.setup([button1_pin, button2_pin], GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 버튼에 내부 풀업 저항 사용

# 모터1 회전
def motor1_spin():
    GPIO.output(motor1_input1_pin, GPIO.HIGH)  # 모터1의 IN1 핀을 HIGH로 설정
    GPIO.output(motor1_input2_pin, GPIO.LOW)  # 모터1의 IN2 핀을 LOW로 설정

# 모터1 정지
def motor1_stop():
    GPIO.output(motor1_input1_pin, GPIO.LOW)  # 모터1의 IN1 핀을 LOW로 설정
    GPIO.output(motor1_input2_pin, GPIO.LOW)  # 모터1의 IN2 핀을 LOW로 설정

# 모터2 회전
def motor2_spin():
    GPIO.output(motor2_input1_pin, GPIO.HIGH)  # 모터2의 IN1 핀을 HIGH로 설정
    GPIO.output(motor2_input2_pin, GPIO.LOW)  # 모터2의 IN2 핀을 LOW로 설정

# 모터2 정지
def motor2_stop():
    GPIO.output(motor2_input1_pin, GPIO.LOW)  # 모터2의 IN1 핀을 LOW로 설정
    GPIO.output(motor2_input2_pin, GPIO.LOW)  # 모터2의 IN2 핀을 LOW로 설정

# LED 켜기
def led_on():
    GPIO.output(led_pin, GPIO.HIGH)  # LED 핀을 HIGH로 설정하여 LED를 켜기

# LED 끄기
def led_off():
    GPIO.output(led_pin, GPIO.LOW)  # LED 핀을 LOW로 설정하여 LED를 끄기

try:
    motor_state = False  # 모터 상태 변수 (작동: True, 정지: False)
    led_state = False  # LED 상태 변수 (켜짐: True, 꺼짐: False)
    button1_flag = False  # 버튼1의 눌림 상태를 표시하는 변수
    button2_flag = False  # 버튼2의 눌림 상태를 표시하는 변수

    while True:
        button1_state = GPIO.input(button1_pin)  # 버튼1 상태 읽기
        button2_state = GPIO.input(button2_pin)  # 버튼2 상태 읽기

        if button1_state == GPIO.LOW and not button1_flag:
            # 버튼1이 눌리고 이전에 눌리지 않은 상태일 때 실행
            button1_flag = True
            motor_state = not motor_state  # 모터 상태를 반전시킴

            if motor_state:
                motor1_spin()  # 모터1과 모터2를 회전시킴
                motor2_spin()
            else:
                motor1_stop()  # 모터1과 모터2를 정지시킴
                motor2_stop()

        elif button1_state == GPIO.HIGH:
            # 버튼1이 눌리지 않은 상태로 전환되면 flag를 초기화
            button1_flag = False

        if button2_state == GPIO.LOW and not button2_flag:
            # 버튼2가 눌리고 이전에 눌리지 않은 상태일 때 실행
            button2_flag = True
            led_state = not led_state  # LED 상태를 반전시킴

            if led_state:
                led_on()  # LED 켜기
            else:
                led_off()  # LED 끄기

        elif button2_state == GPIO.HIGH:
            # 버튼2가 눌리지 않은 상태로 전환되면 flag를 초기화
            button2_flag = False

        time.sleep(0.1)  # 디바운스를 위한 딜레이

except KeyboardInterrupt:
    GPIO.cleanup()