import serial
import time
import logging
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', 
        level=logging.INFO, 
        datefmt='%Y-%m-%d %H:%M:%S')

PIN_20 = 18 # GPIO 18 in GPIO.BCM mode; PIN 12 in GPIO.BOARD mode.

up =  bytearray(b'\x9b\x06\x02\x01\x00\xfc\xa0\x9d')
down = bytearray(b'\x9b\x06\x02\x02\x00\x0c\xa0\x9d')
wake_up = bytearray(b'\x9b\x06\x02\x00\x00\x6c\xa1\x9d')
# preset1 is set to lowest height (sitting)
# preset2 is set to middle height (reading)
# preset3 is set to high height (standing/rest)
preset1 = bytearray(b'\x9b\x06\x02\x04\x00\xac\xa3\x9d')
preset2 = bytearray(b'\x9b\x06\x02\x08\x00\xac\xa6\x9d')
preset3 = bytearray(b'\x9b\x06\x02\x10\x00\xac\xac\x9d')

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


def report_heights(serial0):
    current_signal = b''
    char = b''
    heights = []
    while serial0.in_waiting and (char != b'\x9d' or len(current_signal) == 0):
        char = serial0.read(1)
        if char == b'\x9b':
            # starts a new signal if \x9d is observed.
            current_signal = char
        elif char != b'\x9d':
            current_signal += char
        else:
            current_signal += char
            # height signal should have length of 9 chars.
            if len(current_signal) != 9: 
                current_signal = b''
                continue
            # add to heights if it's different from last one.
            height = signal2height(current_signal)
            if True: # len(heights) == 0 or heights[-1] != height:
                heights.append(height)
                print(current_signal, height)
            # then reinitialize current_signal
            current_signal = b''
    return heights


def setup():
    # Or GPIO.BOARD - GPIO Numbering vs Pin numbering
    GPIO.setmode(GPIO.BCM)

    # Turn desk in operating mode by setting controller pin20 to HIGH
    # This will allow us to send commands and to receive the current height
    GPIO.setup(PIN_20, GPIO.OUT)
    # Set up serial communication.
    SERIAL_PORT = "/dev/ttyS0" # GPIO14 (TX) and GPIO15 (RX)
    serial0 = serial.Serial(SERIAL_PORT, 9600, timeout=500)
    return serial0


def teardown():
    GPIO.cleanup()

def measure_height():
    # setup serial
    serial0 = setup()
    # wake up the desk
    GPIO.output(PIN_20, GPIO.HIGH)
    time.sleep(.5)
    serial0.write(wake_up)
    time.sleep(.5)
    GPIO.output(PIN_20, GPIO.LOW)
    print(serial0.in_waiting)
    heights = report_heights(serial0)
    return heights


def run_mode(work, serial0):
    if work:
        logging.info('Going down to work for 50 mins...')
        if not GPIO.input(PIN_20):
            logging.info('desk inactive, activating desk...')
            GPIO.output(PIN_20, GPIO.HIGH)
        serial0.write(preset1*10)
        time.sleep(3000)
    else:
        logging.info('Going up to rest 10 mins...')
        if not GPIO.input(PIN_20):
            logging.info('desk inactive, activating desk...')
            GPIO.output(PIN_20, GPIO.HIGH)
        serial0.write(preset3*10)
        time.sleep(600)


def run_schedule(rounds):
    serial0 = setup()
    GPIO.output(PIN_20, GPIO.HIGH)
    iteration = 0
    while iteration < rounds:
        run_mode(iteration % 2, serial0)
        # after one round of work and rest, increment by 1 iteration.
        iteration += 1
    teardown()


if __name__ == "__main__":
    run_schedule(8)
