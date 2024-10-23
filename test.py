from openai import OpenAI
import RPi.GPIO as GPIO
import time
from gtts import gTTS
import os
from dotenv import load_dotenv

load_dotenv()

load_dotenv('gpio.env')


MOTOR_MOUTH_ENA = 29  # Physical pin 29 (GPIO 5)
MOTOR_MOUTH_IN1 = 31  # Physical pin 31 (GPIO 6)
MOTOR_MOUTH_IN2 = 33  # Physical pin 33 (GPIO 13) - PWM1
MOTOR_BODY_IN3 = 35   # Physical pin 37 (GPIO 26)
MOTOR_BODY_IN4 = 37   # Physical pin 16 (GPIO 23) - Assuming this is still correct
MOTOR_BODY_ENB = 32   # Physical pin 32 (GPIO 12)

# Audio Detector - You might need to adjust this if it's connected differently
AUDIO_DETECTOR = 36   # Physical pin 7 (GPIO 4) - This is just a placeholder, adjust as needed

print(MOTOR_MOUTH_ENA, MOTOR_MOUTH_IN1, MOTOR_MOUTH_IN2, MOTOR_BODY_IN3, MOTOR_BODY_IN4, MOTOR_BODY_ENB, AUDIO_DETECTOR)

GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
GPIO.setup(MOTOR_MOUTH_ENA, GPIO.OUT)
GPIO.setup(MOTOR_MOUTH_IN1, GPIO.OUT)
GPIO.setup(MOTOR_MOUTH_IN2, GPIO.OUT)
GPIO.setup(MOTOR_BODY_IN3, GPIO.OUT)
GPIO.setup(MOTOR_BODY_IN4, GPIO.OUT)
GPIO.setup(MOTOR_BODY_ENB, GPIO.OUT)
GPIO.setup(AUDIO_DETECTOR, GPIO.IN)

def move_mouth():
    # Enable motor (MOTOR_MOUTH_ENA)
    GPIO.output(MOTOR_MOUTH_ENA, GPIO.HIGH)

    # Set direction for the mouth movement
    GPIO.output(MOTOR_MOUTH_IN1, GPIO.HIGH)  # Forward
    GPIO.output(MOTOR_MOUTH_IN2, GPIO.LOW)   # Ensure opposite direction pin is LOW

    # Run for a short period of time
    time.sleep(0.5)

    # Stop the motor
    GPIO.output(MOTOR_MOUTH_ENA, GPIO.LOW)   # Disable motor
    GPIO.output(MOTOR_MOUTH_IN1, GPIO.LOW)   # Stop movement

def move_head():
    # Enable motor (MOTOR_BODY_ENB)
    GPIO.output(MOTOR_BODY_ENB, GPIO.HIGH)

    # Set direction for the head movement
    GPIO.output(MOTOR_BODY_IN3, GPIO.HIGH)  # Forward
    GPIO.output(MOTOR_BODY_IN4, GPIO.LOW)   # Ensure opposite direction pin is LOW

    # Run for a short period of time
    time.sleep(0.5)

    # Stop the motor
    GPIO.output(MOTOR_BODY_ENB, GPIO.LOW)   # Disable motor
    GPIO.output(MOTOR_BODY_IN3, GPIO.LOW)   # Stop movement

def move_tail():
    # Enable motor (MOTOR_BODY_ENB)
    GPIO.output(MOTOR_BODY_ENB, GPIO.HIGH)

    # Set direction for the tail movement
    GPIO.output(MOTOR_BODY_IN4, GPIO.HIGH)  # Forward
    GPIO.output(MOTOR_BODY_IN3, GPIO.LOW)   # Ensure opposite direction pin is LOW

    # Run for a short period of time
    time.sleep(0.5)

    # Stop the motor
    GPIO.output(MOTOR_BODY_ENB, GPIO.LOW)   # Disable motor
    GPIO.output(MOTOR_BODY_IN4, GPIO.LOW)   # Stop movement


def main():
    while True:
        test_all_movements()
        
        
def test_all_movements():
    try:
        print("Starting continuous movement test. Press CTRL+C to stop.")
        while True:
            # Move mouth
            GPIO.output(MOTOR_MOUTH_ENA, GPIO.HIGH)
            GPIO.output(MOTOR_MOUTH_IN1, GPIO.HIGH)
            GPIO.output(MOTOR_MOUTH_IN2, GPIO.LOW)
            
            # Move head
            GPIO.output(MOTOR_BODY_ENB, GPIO.HIGH)
            GPIO.output(MOTOR_BODY_IN3, GPIO.HIGH)
            GPIO.output(MOTOR_BODY_IN4, GPIO.LOW)
            
            time.sleep(1)  # Run for 1 second
            
            # Stop mouth movement
            GPIO.output(MOTOR_MOUTH_ENA, GPIO.LOW)
            
            # Move tail (reverse head/tail movement)
            GPIO.output(MOTOR_BODY_IN3, GPIO.LOW)
            GPIO.output(MOTOR_BODY_IN4, GPIO.HIGH)
            
            time.sleep(1)  # Run for 1 second
            
            # Stop body movement
            GPIO.output(MOTOR_BODY_ENB, GPIO.LOW)
            
    except KeyboardInterrupt:
        print("\nTest stopped by user.")
    finally:
        # Turn off all motors
        GPIO.output(MOTOR_MOUTH_ENA, GPIO.LOW)
        GPIO.output(MOTOR_BODY_ENB, GPIO.LOW)
        GPIO.output(MOTOR_MOUTH_IN1, GPIO.LOW)
        GPIO.output(MOTOR_MOUTH_IN2, GPIO.LOW)
        GPIO.output(MOTOR_BODY_IN3, GPIO.LOW)
        GPIO.output(MOTOR_BODY_IN4, GPIO.LOW)
        print("All motors stopped.")
        raise SystemExit  # This will ensure the program exits after cleanup

if __name__ == "__main__":
    try:
        test_all_movements()
    finally:
        print("Cleaning up GPIO")
        GPIO.cleanup()