
from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import requests

app = Flask(__name__)

데이터 = {
    'temperature': [25, 28, 20, 30, 22, 26, 27, 23, 21, 29],
    'weight': [4, 6, 3, 5, 4.5, 5.5, 6.5, 3.5, 4, 5.5],
    'humidity': [50, 60, 40, 65, 55, 45, 70, 30, 50, 75],
    'predicted_time': [2, 3, 1.5, 3.5, 2.2, 2.8, 3.2, 2.1, 1.8, 3.3] #분
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

        new_data = pd.DataFrame({'temperature': [temperature], 'weight': [weight], 'humidity': [humidity]})
        predict = model.predict(new_data)
        predicted_time = predict[0]*60
        print(predicted_time)
        s_server = {
            "predicted_time": predicted_time
        }
        original_server_url = 'http://192.168.21.245:5014/'# 보내는 서버

        # 원래 서버로 POST 요청 보내기
        response_to_original_server = requests.post(original_server_url, json=s_server)
        if response_to_original_server.status_code == 200:
            print("원래 서버로의 요청이 성공적으로 전송되었습니다.")
        else:
            print("원래 서버로의 요청 전송 실패:", response_to_original_server.status_code)
    return jsonify({"message": "데이터 전송 완료"})  # 예시 응답 메시지


if __name__ == '__main__':
    app.run(host='192.168.20.37', port=5017) #내 서버