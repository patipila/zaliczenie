import speech_recognition as sr  # To convert speech into text
import pyttsx3  # To convert text into speech
import datetime  # To get the date and time
import os  # To open files
import time  # To calculate time
import subprocess  # To open files
from tkinter import *  # For the graphics
import pyjokes  # For some really bad jokes
from playsound import playsound  # To playsound
import webbrowser
import wikipedia
import requests
import pyowm
import keyboard  # To get keyboard

name_file = open("Assistant_name", "r")
name_assistant = name_file.read()

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def get_location():
    """ Function To Print GeoIP Latitude & Longitude """
    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    my_ip = ip_request.json()['ip']
    geo_request = requests.get('https://get.geojs.io/v1/ip/geo/' +my_ip + '.json')
    geo_data = geo_request.json()
    geo = geo_data['city']
    return geo


def speak(text):
    engine.say(text)
    print(name_assistant + " : "  +  text)
    engine.runAndWait()


def wishMe():
    hour = datetime.datetime.now().hour

    if hour >= 0 and hour < 12:
        speak("Hello, I am " + name_assistant + ". Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Hello, I am " + name_assistant + ". Good Afternoon")
    else:
        speak("Hello, I am " + name_assistant + ". Good Evening")


def get_audio():
    r = sr.Recognizer()
    audio = ''

    with sr.Microphone() as source:
        print("Listening")
        playsound("whole.mp3")
        audio = r.listen(source, phrase_time_limit=10)
        playsound("assistant_off.mp3")
        print("Stop.")

    try:
        text = r.recognize_google(audio, language='en-US')
        print('You: ' + ': ' + text)
        return text
    except:
        return


def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"

    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])


def date():
    now = datetime.datetime.now()
    month_name = now.month
    day_name = now.day
    month_names = (
    'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
    'December',)
    ordinalnames = (
    '1st', '2nd', '3rd', ' 4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th', '14th', '15th',
    '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23rd', '24rd', '25th', '26th', '27th', '28th', '29th',
    '30th', '31st',)

    speak("Today is " + month_names[month_name - 1] + " " + ordinalnames[day_name - 1] + '.')

wishMe()

def process_audio():
    run = 1
    if __name__ == '__main__':
        while True:

            statement = get_audio().lower()

            if "hello" in statement or "hi" in statement:
                wishMe()

            if "goodbye" in statement or "ok bye" in statement or "stop" in statement:
                speak('Your personal assistant ' + name_assistant + ' is shutting down, Good bye')
                screen.destroy()
                break


            if 'joke' in statement:
                speak(pyjokes.get_joke())

            if 'youtube' in statement:
                webbrowser.open("https://www.youtube.com", new=2)
                speak("youtube is open now")
                time.sleep(5)

            if 'google' in statement:
                webbrowser.open("https://www.google.com", new=2)
                speak("Google is open now")
                time.sleep(5)

            if 'gmail' in statement:
                webbrowser.open("mail.google.com", new=2)
                speak("Google Mail open now")
                time.sleep(5)

            if 'netflix' in statement:
                webbrowser.open("netflix.com", new=2)
                speak("Netflix open now")

            if 'open prime video' in statement:
                webbrowser.open("primevideo.com", new=2)
                speak("Amazon Prime Video open now")
                time.sleep(5)

            if 'news' in statement:
                news = webbrowser.open("https://www.independent.co.uk/topic/poland", new=2)
                speak('Here are some headlines from the Times of Poland, Happy reading')
                time.sleep(6)

            if 'corona' in statement:
                news = webbrowser.open("https://www.worldometers.info/coronavirus/")
                speak('Here are the latest covid-19 numbers')
                time.sleep(6)

            if 'time' in statement:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"the time is {strTime}")

            if 'date' in statement:
                date()

            if 'who are you' in statement or 'what can you do' in statement:
                speak(
                    'I am ' + name_assistant + ' your personal assistant. I am programmed to minor tasks like opening youtube, google chrome, gmail and search wikipedia etcetra')

            if "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
                speak("I was built by Patrycja and Ola")

            if 'make a note' in statement:
                statement = statement.replace("make a note", "")
                note(statement)

            if 'note this' in statement:
                statement = statement.replace("note this", "")
                note(statement)

            if 'open stackoverflow' in statement:
                speak('opening stackoverflow')
                webbrowser.open('stackoverflow.com')

            if 'weather' in statement:
                city=get_location()
                owm = pyowm.OWM('api-key')  # open weather map API key
                # current weather forecast
                loc = owm.weather_at_place(city)
                weather = loc.get_weather()
                # status
                status = weather.get_detailed_status()
                speak({status} in {city})
                # temperature
                temp = weather.get_temperature(unit='celsius')
                for key, val in temp.items():
                    if key == 'temp':
                        speak("current temperature is {val} degree celcius")
                # humidity, wind, rain, snow
                humidity = weather.get_humidity()
                wind = weather.get_wind()
                speak('humidity is {humidity} grams per cubic meter')
                speak('wind {wind}')
                # sun rise and sun set
                sr = weather.get_sunrise_time(timeformat='iso')
                ss = weather.get_sunset_time(timeformat='iso')
                speak('SunRise time is {sr}')
                speak('SunSet time is {ss}')
                # clouds and rain
                loc = owm.three_hours_forecast(city)
                clouds = str(loc.will_have_clouds())
                rain = str(loc.will_have_rain())
                if clouds == 'True':
                    speak("It may have clouds in next 5 days")
                else:
                    speak("It may not have clouds in next 5 days")
                if rain == 'True':
                    speak("It may rain in next 5 days")
                else:
                    speak("It may not rain in next 5 days")


            if 'wikipedia' in statement:
                if 'open wikipedia' in statement:
                    webbrowser.open('wikipedia.com')
                else:
                    try:
                        speak("searching wikipedia")
                        statement = statement.replace("according to wikipedia", "")
                        results = wikipedia.summary(statement, sentences=2)
                        speak("According to wikipedia")
                        wikipedia_screen(results)
                        speak(results)
                    except Exception:
                        speak('sorry sir could not find any results')
        process_audio()


def change_name():
    name_info = name.get()

    with open("Assistant_name", "w") as file:
        file.write(name_info)

    settings_screen.destroy()
    screen.destroy()


def change_name_window():
    global settings_screen
    global name

    settings_screen = Toplevel(screen)
    settings_screen.title("Settings")
    settings_screen.geometry("300x300")
    settings_screen.iconbitmap('ludzik.ico')

    name = StringVar()

    current_label = Label(settings_screen, text="Current name: " + name_assistant)
    current_label.pack()

    enter_label = Label(settings_screen, text="Please enter your Virtual Assistant's name below")
    enter_label.pack(pady=10)

    Name_label = Label(settings_screen, text="Name")
    Name_label.pack(pady=10)

    name_entry = Entry(settings_screen, textvariable=name)
    name_entry.pack()

    change_name_button = Button(settings_screen, text="Ok", width=10, height=1, command=change_name)
    change_name_button.pack(pady=10)

def wikipedia_screen(text):


  wikipedia_screen = Toplevel(screen)
  wikipedia_screen.title(text)
  wikipedia_screen.iconbitmap('app_icon.ico')

  message = Message(wikipedia_screen, text= text)
  message.pack()

def main_screen():
    global screen
    screen = Tk()
    screen.title(name_assistant)
    screen.geometry("500x500")
    screen.iconbitmap('ludzik.ico')

    name_label = Label(text=name_assistant, width=300, bg="violet", fg="white", font=("Calibri", 13))
    name_label.pack()

    microphone_photo = PhotoImage(file="mikro.png")
    microphone_button = Button(image=microphone_photo, command=process_audio)
    microphone_button.pack(pady=10)

    settings_photo = PhotoImage(file="ustawienia.png")
    settings_button = Button(image=settings_photo, command=change_name_window)
    settings_button.pack(pady=10)

    screen.mainloop()


main_screen()

