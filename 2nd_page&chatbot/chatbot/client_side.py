import speech_recognition as sr
import requests
import pyttsx3
from flask import Flask, request, Response, render_template, url_for, redirect


app = Flask(__name__)


def convert_speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak something...")
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


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


server_url = "http://10.212.8.82:80/chat"  # Replace with the server URL
speak("Welcome to the Chatbot!")
speak("How can I assist you?")


@app.route('/')
def index1():
    return render_template('index.html')


@app.route('/handle_request', methods=['GET', 'POST'])
def handle_request():
    print("started")
    # action = request.args.get('action')
    if request.method == 'POST':
        while True:
            user_input = convert_speech_to_text()
            if user_input.lower() == 'exit':
                break
            elif user_input:
                response = requests.post(server_url, json={'user_input': user_input}).json()
                chatbot_response = response.get('response')
                if chatbot_response:
                    print("Chatbot:", chatbot_response)
                    speak(chatbot_response)
        print('Starting the program')
        return 'Program started'


    elif request.method == 'GET':
        flag = True
        while flag:
            flag = False
            break
        print('Stopping the program')
        return 'Program stopped'


if __name__ == '__main__':
    app.run()
