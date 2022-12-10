import utils
import logging
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', 
        level=logging.INFO, 
        datefmt='%Y-%m-%d %H:%M:%S')

rounds = 8

def run_schedule():
    serial0 = utils.setup()
    GPIO.output(utils.PIN_20, GPIO.HIGH)
    iteration = 0
    while iteration < 2*rounds:
        utils.run_mode(iteration % 2, serial0)
        # after one round of work or rest, increment by 1 iteration.
        iteration += 1
    utils.teardown()


if __name__ == "__main__":
    run_schedule()
