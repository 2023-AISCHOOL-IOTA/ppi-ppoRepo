import RPi.GPIO as GPIO
import time

MOTER1_PIN1 = 24
MOTER1_PIN2 = 23
MOTER2_PIN1 = 21
MOTER2_PIN2 = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup([MOTER1_PIN1, MOTER1_PIN2, MOTER2_PIN1, MOTER2_PIN2], GPIO.OUT)

motor_state = False


def command_three(durations):
    print(durations)
     # 만약 모터가 꺼져 있다면
  
    if durations is not None:
        GPIO.output(MOTER1_PIN1, GPIO.HIGH)
        GPIO.output(MOTER1_PIN2, GPIO.LOW)
        GPIO.output(MOTER2_PIN1, GPIO.HIGH)
        GPIO.output(MOTER2_PIN2, GPIO.LOW)
          
        time.sleep(durations)
    
        GPIO.output(MOTER1_PIN1, GPIO.LOW)
        GPIO.output(MOTER1_PIN2, GPIO.LOW)
        GPIO.output(MOTER2_PIN1, GPIO.LOW)
        GPIO.output(MOTER2_PIN2, GPIO.LOW)

        print("Motor turned off")
        print('Received duration:', durations)
        return 'Motor ran for {} seconds'.format(durations)
    else:
        return 'Error: No duration value provided.', 400
