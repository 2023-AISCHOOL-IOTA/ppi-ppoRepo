#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// WiFi 정보 설정
const char* ssid = "3114";
const char* password = "cki921224";

// OpenWeatherMap API 정보
const char* weatherServer = "http://api.openweathermap.org";
const char* weatherApiKey = "5c259fe39c653fa07d0efaa6c8455d1f";

// Define a mapping between city numbers and their IDs
const int NUM_CITIES = 18;
const int cityIds[NUM_CITIES] = {
  1840898, 1835847, 1843561, 1835553, 1845759,
  1835224, 1845457, 1841808, 1844751, 1846265,
  1845136, 1836553, 1843137, 1846986, 1835327,
  1839071, 1833742, 1838519
};

// LED 핀 번호 설정
const int sunnyLedPin = 12; // 맑은 날 LED를 연결한 디지털 핀
const int rainyLedPin = 13; // 비오는 날 LED를 연결한 디지털 핀

void setup() {
  Serial.begin(115200);
  pinMode(sunnyLedPin, OUTPUT);
  pinMode(rainyLedPin, OUTPUT);
  connectWiFi();
}

void loop() {
  if (Serial.available()) {
    String inputStr = Serial.readStringUntil('\n');
    int cityNumber = inputStr.toInt();
    if (cityNumber >= 1 && cityNumber <= NUM_CITIES) {
      int cityId = cityIds[cityNumber - 1]; // Adjust for array indexing
      Serial.print("Fetching weather for city ID: ");
      Serial.println(cityId);
      getWeather(cityId);
    } else {
      Serial.println("Invalid city number.");
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

void getWeather(int cityId) {
  // OpenWeatherMap API 호출
  String weatherUrl = String(weatherServer) + "/data/2.5/weather?id=" + String(cityId) + "&units=metric&appid=" + String(weatherApiKey);
  HTTPClient weatherHttp;
  weatherHttp.begin(weatherUrl);
  int weatherHttpCode = weatherHttp.GET();

  if (weatherHttpCode > 0) {
    if (weatherHttpCode == HTTP_CODE_OK) {
      String weatherPayload = weatherHttp.getString();
      parseWeatherData(weatherPayload);
    }
  } else {
    Serial.println("Weather API request failed.");
  }

  weatherHttp.end();
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

  // 맑은 날이면 첫 번째 LED를 켭니다.
  if (weatherDescription.indexOf("clear") != -1) {
    digitalWrite(sunnyLedPin, HIGH);
    digitalWrite(rainyLedPin, LOW);
  }
  // 비오는 날이면 두 번째 LED를 켭니다.
  else if (weatherDescription.indexOf("rain") != -1) {
    digitalWrite(sunnyLedPin, LOW);
    digitalWrite(rainyLedPin, HIGH);
  }
  // 그 외의 경우 모든 LED를 끕니다.
  else {
    digitalWrite(sunnyLedPin, LOW);
    digitalWrite(rainyLedPin, LOW);
  }
}