#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// WiFi 정보 설정
const char* ssid = "3114";
const char* password = "cki921224";

// OpenWeatherMap API 정보
const char* server = "http://api.openweathermap.org";
const char* apiKey = "5c259fe39c653fa07d0efaa6c8455d1f";


String city = ""; // 사용자 입력을 저장할 변수

// LED 핀 번호 설정
const int sunnyLedPin = 12; // 맑은 날 LED를 연결한 디지털 핀
const int rainyLedPin = 13; // 비오는 날 LED를 연결한 디지털 핀
const int dustyLedPin = 14; // 미세먼지 많은 날 LED를 연결한 디지털 핀



void setup() {
  Serial.begin(115200);
  
  pinMode(sunnyLedPin, OUTPUT);
  pinMode(rainyLedPin, OUTPUT);
  pinMode(dustyLedPin, OUTPUT);

  connectWiFi();

}


void loop() {
  if (Serial.available()) {
    char inputChar = Serial.read();
    if (inputChar != '\n') {
      city += inputChar;
    } else {
      Serial.print("Fetching weather for ");
      Serial.println(city);
      getWeather(city);
      city = "";
    }
  }

}

void connectWiFi() {
  Serial.print("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  
  Serial.println("\nWiFi connected.");
}

void getWeather(String cityName) {
  // OpenWeatherMap API 호출
  String url = String(server) + "/data/2.5/weather?q=" + cityName + "&units=metric&appid=" + apiKey;
  HTTPClient http;
  http.begin(url);
  int httpCode = http.GET();

  if (httpCode > 0) {
    if (httpCode == HTTP_CODE_OK) {
      String payload = http.getString();
      parseWeatherData(payload);
    }
  } else {
    Serial.println("HTTP request failed.");
  }

  http.end();
}

void parseWeatherData(String payload) {
  DynamicJsonDocument doc(1024);
  deserializeJson(doc, payload);
  
  String cityName = doc["name"].as<String>();
  double temperature = doc["main"]["temp"].as<double>();
  String weatherDescription = doc["weather"][0]["description"].as<String>();

  Serial.println("City: " + cityName);
  Serial.println("Temperature: " + String(temperature) + " °C");
  Serial.println("Weather: " + weatherDescription);

  // 날씨 상태에 따라 LED 켜기
  // if (weatherDescription.indexOf("clouds") != -1) {       // 'clouds'가 포함되면 LED켜짐
  //   digitalWrite(ledPin, HIGH); // LED를 켭니다.
  // } else {
  //   digitalWrite(ledPin, LOW); // LED를 끕니다.
  // }

  // 맑은 날이면 첫 번째 LED를 켭니다.
  if (weatherDescription.indexOf("clear") != -1) {
    digitalWrite(sunnyLedPin, HIGH);
    digitalWrite(rainyLedPin, LOW);
    digitalWrite(dustyLedPin, LOW);
  }
  // 비오는 날이면 두 번째 LED를 켭니다.
  else if (weatherDescription.indexOf("rain") != -1) {
    digitalWrite(sunnyLedPin, LOW);
    digitalWrite(rainyLedPin, HIGH);
    digitalWrite(dustyLedPin, LOW);
  }
  // 미세먼지 많은 날이면 세 번째 LED를 켭니다.
  else if (weatherDescription.indexOf("dust") != -1) {
    digitalWrite(sunnyLedPin, LOW);
    digitalWrite(rainyLedPin, LOW);
    digitalWrite(dustyLedPin, HIGH);
  }
  // 그 외의 경우 모든 LED를 끕니다.
  else {
    digitalWrite(sunnyLedPin, LOW);
    digitalWrite(rainyLedPin, LOW);
    digitalWrite(dustyLedPin, LOW);
  }

}
