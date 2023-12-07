from flask import Flask, request, jsonify
import RPi.GPIO as GPIO
import time
app = Flask(__name__)

fan_relay_pin = 24
uv_relay_pin = 21

global fan_state, uv_state  # 전역 변수를 수정하기 위해 global 키워드 사용
global all_time, fan_time, uv_time # 전체 동시 동작, 팬 동작, UV 동작 남은 시간
global start_time, stop_time # 타이머에 사용할 변수
global a_count, f_count, u_count

fan_state = False  # 팬 상태를 추적하는 변수 (회전 중: True, 정지: False)
uv_state = False  # UV 상태를 추적하는 변수 (켜짐: True, 꺼짐: False)
all_time = fan_time = uv_time = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup([fan_relay_pin, uv_relay_pin], GPIO.OUT)

def all_on(data):
    GPIO.output([fan_relay_pin, uv_relay_pin], GPIO.LOW)
    fan_state = uv_state = True


def all_on_timer(data):
    GPIO.output([fan_relay_pin, uv_relay_pin], GPIO.LOW)
    fan_state = uv_state = True
    all_time = data['fan_timer']
    all_time = float(all_time)
    
    start_time = time.time()
    end_time = start_time + all_time
    a_count = 0
    while time.time() <= end_time :
        time.sleep(1)
        a_count += 1
        
        if fan_state == False and uv_state == False:
            all_time = float(data['fan_timer']) - a_count
            break
        
    GPIO.output([fan_relay_pin, uv_relay_pin], GPIO.HIGH)
    fan_state = uv_state = False


def all_off(data):
    GPIO.output([fan_relay_pin, uv_relay_pin], GPIO.HIGH)
    fan_state = uv_state = False  # 모터와 LED 상태 초기화
    print("f_code (0) : all_off")


def all_off_timer(data):
    GPIO.output([fan_relay_pin, uv_relay_pin], GPIO.HIGH)
    fan_state = uv_state = False
    
    
def fan_on(data):
    GPIO.output(fan_relay_pin, GPIO.LOW)
    fan_state = True


def fan_on_timer(data):
    GPIO.output(fan_relay_pin, GPIO.LOW)
    fan_state = True
    fan_time = float(data['fan_timer'])
    
    start_time = time.time()
    end_time = start_time + fan_time
    count = 0
    while time.time() <= end_time :
        time.sleep(1)
        count += 1
        fan_time = float(data['fan_timer']) - count
        if fan_state == False:
            break

    GPIO.output(fan_relay_pin, GPIO.HIGH)
    fan_state = False


def fan_off(data):
    GPIO.output(fan_relay_pin, GPIO.HIGH)
    fan_state = False
    fan_time = None

def fan_off_timer(data):
    GPIO.output(fan_relay_pin, GPIO.HIGH)
    fan_state = False



def uv_on(data):
    GPIO.output(uv_relay_pin, GPIO.LOW)
    uv_state = True


def uv_on_timer(data):
    GPIO.output(uv_relay_pin, GPIO.LOW)
    uv_state = True
    uv_time = float(data['uv_timer'])
    
    start_time = time.time()
    end_time = start_time + uv_time
    count = 0
    while time.time() <= end_time :
        time.sleep(1)
        count += 1
        if uv_state == False:
            uv_time = float(data['uv_timer']) - count
            break

    GPIO.output(uv_relay_pin, GPIO.HIGH)
    uv_state = False


def uv_off(data):
    GPIO.output(uv_relay_pin, GPIO.HIGH)
    uv_state = False
    uv_time = None


def uv_off_timer(data):
    GPIO.output(uv_relay_pin, GPIO.HIGH)
    uv_state = False



@app.route('/', methods=['GET', 'POST'])  
def opening():
    
    if request.method == 'POST':
        data = request.get_json()
        cmdno = data.get('f_code')

        fan_time = data.get('fan_timer')
        uv_time = data.get('uv_timer')
        if fan_time is None:
            print("팬 시간 없음", end = "")
        
        elif uv_time is None:
            print("UV 시간 없음", end = "")
        else:
            fan_time = int(fan_time)
            uv_time = int(uv_time)
            print(f"[APP] 팬 시간 : {fan_time} / UV 시간 : {uv_time}")
      
        if cmdno == '0':  # 전체 수동 OFF
            all_off(data)
            
        elif cmdno =='1': # 전체 수동 ON
            all_on(data)

        elif cmdno == '2':# 전체 시간 ON
            all_on_timer(data)
            
        elif cmdno == '3': # 전체 시간 OFF
            all_off_timer(data)
            
        elif cmdno == '4': # 팬 수동 ON
            fan_on(data)
            
        elif cmdno == '5': # 팬 수동 OFF 
            fan_off(data)

        elif cmdno == '6': # 팬 시간 ON 
            fan_on_timer(data)

        elif cmdno == '7': # 팬 시간 OFF 
            fan_off_timer(data)

        elif cmdno == '8': # UV 수동 ON
            uv_on(data)
            
        elif cmdno == '9': # UV 수동 OFF 
            uv_off(data)

        elif cmdno == '10': # UV 시간 ON 
            uv_on_timer(data)

        elif cmdno == '11': # UV 시간 OFF 
            uv_off_timer(data)
                
        

        return 'POST request received'

    else:
        return ''
    

@app.route('/time', methods=['GET', 'POST'])
def pred_time():
    if request.method == 'POST':
        data = request.get_json()
        predicted_time = data.get('predicted_time')
        return jsonify(data)



if __name__ == '__main__':
    try:
        app.run(host='192.168.240.248', port=5014)
    finally:
        GPIO.cleanup()  # 서버가 종료되면 GPIO 설정을 초기화