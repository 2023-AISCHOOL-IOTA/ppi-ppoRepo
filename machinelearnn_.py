from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import requests

app = Flask(__name__)

데이터 = {
    'temperature': [28.8, 28.8, 28.7, 28.7, 29,28.8,28.7,25.1,23,23,25,26.4,25.2,24.7,24.4,24.2,24.1,23.5,24.6,26,26.2],
    'weight': [96,93.6,91,93.6,94.9,93.7,93.7,92.3,93.5,94,96.9,96.5,95.5,96.4,96.8,94.8,94.8,96.3,96.5,96.4],
    'humidity': [70.6,70,75.3,72.3,71.1,75.4,74,59.7,57.1,55.1,62.2,47.1,48.7,46,58.5,65.3,52.5,47.7,56.4,63.9],
    'predicted_time': [42,36,38,42,38,41,40,23,30,30,40,26,27,29,30,34,31,28,33,35]
        }

df = pd.DataFrame(데이터)

X = df.drop(columns=['predicted_time'])
y = df['predicted_time']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("평균 제곱 오차:", mse)
print("R-제곱:", r2)

@app.route('/', methods=['GET','POST'])
def predict_drying_time():
    if request.method == 'POST':
        data = request.get_json()
        temperature = int(data['temperature'])
        humidity = int(data['humidity'])
        weight = int(data['weight'])
        print(data)
        
        
        
        
        

        new_data = pd.DataFrame({'temperature': [temperature], 'weight': [weight], 'humidity': [humidity]})
        predict = model.predict(new_data)
        predicted_time = roundf(predict[0],1)*60
        print(predicted_time)
        predicted_time = {
            "predicted_time": (predicted_time)
        }
        original_server_url = 'http://192.168.211.215:5014/time' #보내는 서버

        # 원래 서버로 POST 요청 보내기
        response_to_original_server = requests.post(original_server_url, json=predicted_time)
        if response_to_original_server.status_code == 200:
            print("원래 서버로의 요청이 성공적으로 전송되었습니다.")
        else:
            print("원래 서버로의 요청 전송 실패:", response_to_original_server.status_code)
    return ""  # 예시 응답 메시지


if __name__ == '__main__':
    try:
        app.run(host='192.168.100.79', port=5017) #내 플라스크 서버
    finally:
        clearup()

