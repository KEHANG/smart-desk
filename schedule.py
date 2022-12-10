import utils
import logging
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', 
        level=logging.INFO, 
        datefmt='%Y-%m-%d %H:%M:%S')

rounds = 8
WORK_MODE = 1
REST_MODE = 0
timeouts = {WORK_MODE: 50, REST_MODE: 10}

def run_schedule():
    serial0 = utils.setup()
    GPIO.output(utils.PIN_20, GPIO.HIGH)
    iteration = 0
    while iteration < 2*rounds:
        mode = iteration % 2
        utils.run_mode(mode, serial0, timeouts[mode])
        # after one round of work or rest, increment by 1 iteration.
        iteration += 1
    utils.teardown()


if __name__ == "__main__":
    run_schedule()
