import utils
import intent_detection
import logging
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')


def execute(intent, **kwargs):

	if intent == 'height_report':
		print(utils.measure_height())
	elif intent == 'work':
		utils.run_mode(work=True, timeout=kwargs.get('timeout'))
		utils.run_mode(work=False, timeout=0)
	elif intent == 'rest':
		utils.run_mode(work=False, timeout=kwargs.get('timeout'))
		utils.run_mode(work=True, timeout=0)


if __name__ == "__main__":
    # setup board and pin
    utils.setup_board()
    text = intent_detection.speech_recognition()
    intent, kwargs = intent_detection.detect_intent(text)
    print(intent, kwargs)
    execute(intent, **kwargs)
