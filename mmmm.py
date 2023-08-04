from flask import Flask, request
import RPi.GPIO as GPIO

app = Flask(__name__)

MOTER1_PIN1 = 24
MOTER1_PIN2 = 23
MOTER2_PIN1 = 21
MOTER2_PIN2 = 20
LED_PIN = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup([MOTER1_PIN1, MOTER1_PIN2, MOTER2_PIN1, MOTER2_PIN2, LED_PIN], GPIO.OUT)

motor_state = False  # 모터 상태를 추적하는 변수 (회전 중: True, 정지: False)
led_state = False  # LED 상태를 추적하는 변수 (켜짐: True, 꺼짐: False)

def motor_on_for(seconds):
    GPIO.output(MOTER1_PIN2, GPIO.HIGH)
    GPIO.output(MOTER2_PIN2, GPIO.HIGH) # 모터 켜기
    time.sleep(seconds)  # 지정된 시간 동안 대기
    GPIO.output(MOTER1_PIN1, GPIO.LOW)
    GPIO.output(MOTER2_PIN1, GPIO.LOW)
    

@app.route('/', methods=['GET', 'POST'])  
def opening():
    global motor_state, led_state  # 전역 변수를 수정하기 위해 global 키워드 사용

    if request.method == 'POST':
        data = request.get_json()
        command = data.get('f_code')
        durations = int(data.get('duration'))
        print(durations)
        if command == '1':
            if motor_state:  # 모터가 이미 회전 중인 경우
                GPIO.output([MOTER1_PIN1, MOTER1_PIN2, MOTER2_PIN1, MOTER2_PIN2], GPIO.LOW)  # 모터 정지
            else:  # 모터가 정지 상태인 경우
                GPIO.output(MOTER1_PIN1, GPIO.HIGH)  # 모터1 회전
                GPIO.output(MOTER2_PIN1, GPIO.HIGH)  # 모터2 회전
            motor_state = not motor_state  # 모터 상태 반전

        elif command == '2':
            if led_state:  # LED가 이미 켜져 있는 경우
                GPIO.output(LED_PIN, GPIO.LOW)  # LED 끄기
            else:  # LED가 꺼져 있는 경우
                GPIO.output(LED_PIN, GPIO.HIGH)  # LED 켜기
            led_state = not led_state  # LED 상태 반전
            
        elif command == '0':  # 모든 작업 정지
                GPIO.output([MOTER1_PIN1, MOTER1_PIN2, MOTER2_PIN1, MOTER2_PIN2, LED_PIN], GPIO.LOW)
                motor_state = led_state = False  # 모터와 LED 상태 초기화
                
        elif command == '3':
            if duration is not None:
                motor_on_for(duration)  # 지정된 시간 동안 모터를 켬
                return 'Motor ran for {} seconds'.format(duration)
            else:
                return 'Error: No duration value provided.', 400  # 잘못된 요청 응답
        else:
            return 'Invalid command.', 400  # 잘못된 명령 응


        return 'POST request received'

    else:
        return ''



if __name__ == '__main__':
    try:
        app.run(host='192.168.20.36', port=5014)
    finally:
        GPIO.cleanup()  # 서버가 종료되면 GPIO 설정을 초기화