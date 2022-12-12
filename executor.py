import utils
import intent_detection
import speech_recognition as sr
import logging
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

def is_wake_word(speech, wake_word):

  return wake_word.lower() in speech.lower()


def execute(intent, **kwargs):

	if intent == 'height_report':
		print(utils.measure_height())
	elif intent == 'work':
		utils.run_mode(work=True, timeout=kwargs.get('timeout'))
		utils.run_mode(work=False, timeout=0)
	elif intent == 'rest':
		utils.run_mode(work=False, timeout=kwargs.get('timeout'))
		utils.run_mode(work=True, timeout=0)
	else:
		print(f"{intent} not supported yet.")


def listen_and_act():
    text = intent_detection.speech_recognition()
    intent, kwargs = intent_detection.detect_intent(text)
    print("Intent detected:", intent, kwargs)
    execute(intent, **kwargs)


def continuous_listen_and_act(wake_word='Emma'):
    #  Create a speech recognition object
    r = sr.Recognizer()

    # Continuously listen for speech
    while True:
      # Listen for speech
      with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

      try:
        # Convert the speech to text
        text = r.recognize_google(audio)
        print("Audio detected:", text)
      except sr.UnknownValueError:
        print("Nothing said. Listening again...")
        continue

      # Check if the wake word is present in the speech
      if is_wake_word(text, wake_word):
        # Wake word has been detected, do something...
        print("Wake word detected:", text)
        intent, kwargs = intent_detection.detect_intent(text)
        print("Intent detected:", intent, kwargs)
        execute(intent, **kwargs)


if __name__ == "__main__":
    # setup board and pin
    utils.setup_board()
    continuous_listen_and_act()
