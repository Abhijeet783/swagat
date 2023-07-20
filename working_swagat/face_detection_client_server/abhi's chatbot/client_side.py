import speech_recognition as sr
import requests
import pyttsx3
from flask import Flask, request, Response, render_template, url_for, redirect
stop_flag=0

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


server_url = "http://10.212.10.188:5001/chat"  # Replace with the server URL



@app.route('/')
def index1():
    return render_template('index.html')


@app.route('/handle_request', methods=['GET', 'POST'])
def handle_request():
    # action = request.args.get('action')
    global stop_flag
    stop_flag=0
    print(stop_flag)
    if request.method == 'POST':
        print("started")
        speak("Welcome to the Chatbot!")
        speak("How can I assist you?")
        while not stop_flag:
                user_input = convert_speech_to_text()
                if user_input.lower() == 'exit':
                    break
                elif user_input:
                    response = requests.post(server_url, json={'user_input': user_input}).json()
                    print('request sent')
                    chatbot_response = response.get('response')
                    if chatbot_response:
                        print("Chatbot:", chatbot_response)
                        speak(chatbot_response)
        print('program waitng for user input')
        return 'Program started'


@app.route('/handle_request2', methods=['GET', 'POST'])
def handle_request2():
        global stop_flag
        if request.method == 'POST':
            print(stop_flag)
            speak("nice to meet with you!  Thank you! ")
            print('Stopping the program')
            stop_flag=1
            return 'Program stopped'


if __name__ == '__main__':
    app.run()
