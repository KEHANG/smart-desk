import serial
import time
import RPi.GPIO as GPIO

SERIAL_PORT = "/dev/ttyS0" # GPIO14 (TX) and GPIO15 (RX)
PIN_20 = 18 # GPIO 18 in GPIO.BCM mode; PIN 12 in GPIO.BOARD mode.

up =  bytearray(b'\x9b\x06\x02\x01\x00\xfc\xa0\x9d')
down = bytearray(b'\x9b\x06\x02\x02\x00\x0c\xa0\x9d')
wake_up = bytearray(b'\x9b\x06\x02\x00\x00\x6c\xa1\x9d')


def main():
    serial0 = serial.Serial(SERIAL_PORT, 9600, timeout=500)
    # Or GPIO.BOARD - GPIO Numbering vs Pin numbering
    GPIO.setmode(GPIO.BCM)

    # Turn desk in operating mode by setting controller pin20 to HIGH
    # This will allow us to send commands and to receive the current height
    GPIO.setup(PIN_20, GPIO.OUT)
    GPIO.output(PIN_20, GPIO.HIGH)
    serial0.write(down * 300)
    iteration = 0
    while iteration < 5:
        if iteration % 2:
            print('Going up to rest 10 mins...')
            serial0.write(up * 300)
            time.sleep(6)
        else:
            print('Going down to work for 50 mins...')
            serial0.write(down * 300)
            time.sleep(30)
        iteration += 1
    GPIO.cleanup()


if __name__ == "__main__":
    main()
