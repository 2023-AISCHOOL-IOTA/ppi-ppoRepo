#include <TFT_eSPI.h>

// TFT LCD 모듈 연결 핀 설정
#define TFT_CS   15
#define TFT_DC   33
#define TFT_RST  -1

TFT_eSPI tft = TFT_eSPI(); // TFT_eSPI 객체 생성

// 모터 핀 설정
const int motorPin = 5;

void setup() {
  tft.begin(); // TFT LCD 모듈 초기화

  tft.setRotation(3); // 디스플레이 회전 설정 (0~3까지의 값, 3으로 설정하여 270도 회전)
  tft.fillScreen(TFT_BLACK); // 배경을 검정색으로 채웁니다.

  tft.setTextSize(2);
  tft.setTextColor(TFT_WHITE);
  tft.setTextDatum(MC_DATUM);

  pinMode(motorPin, OUTPUT); // 모터 핀을 출력으로 설정
}

void loop() {
  int motorTime = getMotorTime(); // 앱에서 입력 받은 모터 작동 시간을 가져옵니다.

  // 모터 작동
  digitalWrite(motorPin, HIGH);

  // 남은 시간 출력
  for (int timeLeft = motorTime; timeLeft >= 0; timeLeft--) {
    drawTime(timeLeft);
    delay(1000); // 1초 대기
  }

  // 모터 정지
  digitalWrite(motorPin, LOW);

  // 작동이 완료되면 디스플레이를 초기화하여 남은 시간을 지웁니다.
  tft.fillScreen(TFT_BLACK);
}

// 앱으로부터 모터 작동 시간을 입력받는 함수 (예시로 10초로 설정)
int getMotorTime() {
  return 10;
}

// 남은 시간 표시 함수
void drawTime(int seconds) {
  int minutes = seconds / 60;
  int secs = seconds % 60;

  // 이전에 표시한 시간을 지우고 새로운 시간을 표시합니다.
  tft.fillRect(0, 100, tft.width(), 40, TFT_BLACK);
  tft.drawString(String(minutes) + ":" + String(secs, 2), tft.width() / 2, 120);
}