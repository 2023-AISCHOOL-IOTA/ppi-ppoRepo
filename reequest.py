import requests

def send_data_to_server():
    # 보낼 JSON 데이터
    data_to_send = {'temperature': 30, 'humidity': 90}

    # 두 번째 플라스크 서버 URL (두 번째 서버의 주소와 포트를 변경해야 합니다)
    second_server_url = 'http://196.00.00.00/'

    # 두 번째 플라스크 서버로 POST 요청 보내기
    response = requests.post(second_server_url, json=data_to_send)

    if response.status_code == 200:
        print('Data sent successfully to the second server')
    else:
        print('Failed to send data to the second server')

if __name__ == '__main__':
    send_data_to_server()