import serial
import time
import RPi.GPIO as GPIO

PIN_20 = 18 # GPIO 18 in GPIO.BCM mode; PIN 12 in GPIO.BOARD mode.

up =  bytearray(b'\x9b\x06\x02\x01\x00\xfc\xa0\x9d')
down = bytearray(b'\x9b\x06\x02\x02\x00\x0c\xa0\x9d')
wake_up = bytearray(b'\x9b\x06\x02\x00\x00\x6c\xa1\x9d')


def signal2height(signal):

    payload = signal[3:-3]
    decrypt = ""
    _SEG = ["3f", "06", "5b", "4f", "66", 
            "6d", "7d", "07", "7f", "6f", "77", 
            "7c", "39", "5e", "79", "71"]
    for i , c in enumerate(payload):
        c = format(c, '#04x')[2:]
        if c in _SEG:
            decrypt += str(_SEG.index(c))
        else:
            j = hex(int(c[0], 16) - 0x08)[2:]
            decrypt += str(_SEG.index(j + c[1])) 
            decrypt += "."
    return decrypt


def report_heights():
    serial0 = setup()
    current_signal = b''
    char = b''
    heights = []
    while char != b'\x9d' or len(current_signal) == 0:
        char = serial0.read(1)
        current_signal += char
        if char == b'\x9b':
            # starts a new signal if \x9d is observed.
            current_signal = char
        if char == b'\x9d':
            # add to heights if it's different from last one.
            if len(heights) == 0 or heights[-1] != current_signal:
                if len(current_signal) == 9:
                    heights.append(current_signal)
                    print(current_signal, signal2height(current_signal))
            # then reinitialize current_signal
            current_signal = b''

def setup():
    # Or GPIO.BOARD - GPIO Numbering vs Pin numbering
    GPIO.setmode(GPIO.BCM)

    # Turn desk in operating mode by setting controller pin20 to HIGH
    # This will allow us to send commands and to receive the current height
    GPIO.setup(PIN_20, GPIO.OUT)
    GPIO.output(PIN_20, GPIO.HIGH)
    # Set up serial communication.
    SERIAL_PORT = "/dev/ttyS0" # GPIO14 (TX) and GPIO15 (RX)
    serial0 = serial.Serial(SERIAL_PORT, 9600, timeout=500)
    return serial0


def teardown():
    GPIO.cleanup()


def run_schedule():
    serial0 = setup()
    serial0.write(down * 300)
    iteration = 0
    while iteration < 5:
        print('Going up to rest 10 mins...')
        serial0.write(up * 300)
        time.sleep(600)
        print('Going down to work for 50 mins...')
        serial0.write(down * 300)
        time.sleep(3000)
        iteration += 1
    teardown()


if __name__ == "__main__":
    run_schedule()
