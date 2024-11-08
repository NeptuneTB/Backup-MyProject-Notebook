import RPi.GPIO as GPIO
import time

stepPin = 5
dirPin = 2
enPin = 8
initialPosition = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(stepPin, GPIO.OUT)
GPIO.setup(dirPin, GPIO.OUT)
GPIO.setup(enPin, GPIO.OUT)
GPIO.output(enPin, GPIO.LOW)

def move_motor(steps):
    if steps != 0:
        direction = GPIO.HIGH if steps > 0 else GPIO.LOW
        steps = abs(steps)

        print(f"Moving motor {steps} steps {'forward' if direction == GPIO.HIGH else 'reverse'}")

        GPIO.output(dirPin, direction)

        for x in range(initialPosition):
            GPIO.output(stepPin, GPIO.HIGH)
            time.sleep(0.0005)
            GPIO.output(stepPin, GPIO.LOW)
            time.sleep(0.0005)

        for x in range(steps):
            GPIO.output(stepPin, GPIO.HIGH)
            time.sleep(0.0005)
            GPIO.output(stepPin, GPIO.LOW)
            time.sleep(0.0005)

        time.sleep(1)
        print("Movement complete")

try:
    while True:
        user_input = input("Enter steps: ")
        steps_to_move = int(user_input)
        move_motor(steps_to_move)

except KeyboardInterrupt:
    GPIO.cleanup()
