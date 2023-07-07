import json
import random
import speech_recognition as sr
import pyttsx3
import datetime

def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def generate_response(user_input, data):
    for pattern_response in data:
        pattern = pattern_response['pattern']
        responses = pattern_response['responses']
        for pattern in pattern:
            if pattern.lower() in user_input.lower():
                return random.choice(responses)
    return "I'm sorry, but I don't understand."


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("speak something..")
        speak("speak something..")
        audio = recognizer.listen(source)
    try:
        user_input = recognizer.recognize_google(audio)
        print("User:", user_input)
        return user_input
    except sr.UnknownValueError:
        print("Sorry, I could not understand your speech.")
        return ""
    except sr.RequestError:
        print("Sorry, I am unable to process your request.")
        return ""

current_date_time = datetime.datetime.now()
formatted_date_time = current_date_time.strftime("%Y-%m-%d %H:%M:%S")
speak("Welcome to Centre for Development of Advanced Computing Mumbai! We're delighted to have you here")
print("How can I assist you")
speak("How can I assist you")

def chat():
    data = load_data("patterns.json")

    while True:
        user_input = listen()
        if user_input.lower() == 'exit':
            break
        elif user_input.lower()=="time":
            response = f"The current date and time is: {formatted_date_time}"
            print(response)
            speak(response)
        else:
         response = generate_response(user_input, data)
         print("chatbot:",response)
         speak(response)
chat()
