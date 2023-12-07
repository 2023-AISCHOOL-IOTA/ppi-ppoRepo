#include "HX711.h"
#include <DHT.h>

#define DHTPIN 7
#define DHTTYPE DHT11

#define DOUT_PIN 3
#define SCK_PIN 2
 #온습도 코드 
DHT dht(DHTPIN, DHTTYPE);
HX711 scale;

void setup() {
  Serial.begin(9600);
  dht.begin();
  scale.begin(DOUT_PIN, SCK_PIN);
  scale.set_scale(7660);
  scale.tare();
}

void loop() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  long weight = measure_weight();

  double x = calculate_x_from_weight(weight);
  Serial.println(x);


  Serial.print(temperature, 1);
  Serial.print(", ");
  Serial.print(humidity, 0);
  Serial.print(", ");
  Serial.print(x);
}

int duration_time = 100;

long measure_weight() {
  long weight_sum = 0;

  for (int i = 0; i < duration_time; i++) {
    weight_sum += (scale.get_units() * 1000);
  }

  return (long)abs(weight_sum / duration_time);
}

double calculate_x_from_weight(long weight) {
  return (-130.1 + sqrt(130.1 * 130.1 - 4 * (-0.0007) * (-41.223 - weight))) / (2 * (-0.0007));
}