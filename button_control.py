import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정
BUTTON1_PIN = 25  # UV LED 제어 버튼
BUTTON2_PIN = 13  # 펜 제어 버튼
UV_LED_PIN = 21   # UV LED 핀 번호
PEN_PIN = 24      # 펜 핀 번호

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(UV_LED_PIN, GPIO.OUT)
GPIO.setup(PEN_PIN, GPIO.OUT)

uv_led_state = False
pen_state = False

button1_prev_state = True
button2_prev_state = True

try:
    while True:
        button1_state = GPIO.input(BUTTON1_PIN)
        button2_state = GPIO.input(BUTTON2_PIN)

        if button1_state != button1_prev_state:
            if button1_state == GPIO.LOW:
                uv_led_state = not uv_led_state
                GPIO.output(UV_LED_PIN, uv_led_state)
        button1_prev_state = button1_state

        if button2_state != button2_prev_state:
            if button2_state == GPIO.LOW:
                pen_state = not pen_state
                GPIO.output(PEN_PIN, pen_state)
        button2_prev_state = button2_state

        time.sleep(0.01)  # 작은 딜레이를 추가하여 반복 속도 제어

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()