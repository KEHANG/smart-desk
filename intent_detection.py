import speech_recognition as sr
import re


# Define a function to extract time duration information from a text string
def extract_duration(text):
    # Define a regular expression pattern that matches time duration expressions
    duration_pattern = re.compile(r"(\d+)\s*(hours?|hrs?|minute?|minutes?|mins?)")
    # Search for time duration expressions in the text using the regular expression pattern
    duration_matches = duration_pattern.findall(text)

    # If any time duration expressions were found, return the first one
    if len(duration_matches) > 0:
        # Get the numeric value of the duration and the unit (hours or minutes)
        value, unit = duration_matches[0]

        # Return the duration in minutes (1 hour = 60 minutes)
        return int(value) * (60 if unit.startswith("h") else 1)

    # If no time duration expressions were found, return None
    return 0


def speech_recognition():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    text = r.recognize_google(audio)
    print(f"Google Speech Recognition thinks you said: {text}")
    return text


def detect_intent(text):

    # Define the keywords that indicate each intent
    stand_up_keywords = ["stand", "up", "rest"]
    sit_down_keywords = ["sit", "down", "work"]
    report_height_keywords = ["height"]

    # Check if any of the keywords for each intent appear in the text
    if any(word in text for word in stand_up_keywords):
        intent = "rest"
        # Extract the time duration information from the command text
        kwargs = {"timeout": extract_duration(text)}

    elif any(word in text for word in sit_down_keywords):
        intent = "work"
        # Extract the time duration information from the command text
        kwargs = {"timeout": extract_duration(text)}

    elif any(word in text for word in report_height_keywords):
        intent = "height_report"
        kwargs = {}

    print(f"The intent is {intent} with additional arguments: {kwargs}.")

    return intent, kwargs



if __name__ == "__main__":

    text = speech_recognition()
    detect_intent(text)