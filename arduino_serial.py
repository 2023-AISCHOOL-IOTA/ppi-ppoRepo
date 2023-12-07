import requests
import time
import serial

global sensor_temp, sensor_humi, sensor_weight

port = serial.Serial("/dev/ttyACM0", baudrate = 9600, timeout = None)

line = port.readline()
arr = line.split()


sensor_humi = float(arr[0])
sensor_temp = float(arr[1])
sensor_weight = float(arr[2])
        
print(f"h = {sensor_humi} / t = {sensor_temp} / w = {sensor_weight}")
                    
time.sleep(0.01)
    
def send_data_to_server(): # 변수 넣어서 arduino_serial과 병합?
    # 보낼 JSON 데이터
    data_to_send = {'temperature': sensor_temp, 'weight' : sensor_weight, 'humidity': sensor_humi}

    # 두 번째 플라스크 서버 URL (두 번째 서버의 주소와 포트를 변경해야 합니다)
    second_server_url = 'http://192.168.240.78:5017/time'

    # 두 번째 플라스크 서버로 POST 요청 보내기
    response = requests.post(second_server_url, json=data_to_send)

    if response.status_code == 200:
        processed_data = response.text
        print(processed_data)
    else:
        print('Failed to send data to the second server')

        
if __name__ == "__main__":
    send_data_to_server()