from urllib.parse import quote_from_bytes
import pyttsx3
import speech_recognition as sr
import pyaudio
import datetime
import wikipedia
import webbrowser
import os
import smtplib
from decouple import config
from random import choice
from pprint import pprint
from utils import opening_text
import requests
import pyautogui
import time

from fun.os_ops import open_camera, open_cmd, open_notepad

from fun.online_ops import find_my_ip, play_on_youtube,search_on_google,get_random_advice,get_random_joke,send_whatsapp_message,get_latest_news,get_trending_movies,get_weather_report

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices)
print(voices[1].id)
engine.setProperty('voice',voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your desktop assistant. Please tell me how may I help you")


def takeCommand():
    # it takes microphone input from user and returns string output
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
        
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        if not 'exit' in query or 'stop' in query:
            speak(choice(opening_text))
        else:
            speak("Have a good day sir!")
            exit()  
            
       # print(f"User said: {query}\n")
    
    except Exception as e:
        # print(e)
        print("Say that again please...")
        return "None"
    return query

def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your_email@gmail.com','email_password')
    server.sendmail('your_email@gmail.com',to,content)
    server.close();
    

if __name__ == '__main__':
    #speak("madhu how r u")
    wishme()
    if 1:
        query = takeCommand().lower()
    
        #logic for executing tasks based on query
        
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia","")
            results = wikipedia.summary(f'{query}', sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
            
        elif 'open youtube' in query:
            webbrowser.open("www.youtube.com")
            
        elif 'open google' in query:
            webbrowser.open("www.google.com")
        
        elif 'open stackoverflow' in query:
            webbrowser.open("www.stackoverflow.com")
            
        elif  'play music' in query:
            music_dir = 'C:\\Users\\DELL\\Music\\mysongs'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir,songs[0]))
            
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
            
        elif 'open code' in query:
            codePath = "C:\\Users\\DELL\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)
            
            
        elif 'email to madhu' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "receiver_email@gmail.com"
                sendEmail(to,content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry sir. I am not able to send this email")
                
        elif 'open notepad' in query:
            open_notepad()
            
        elif 'open command prompt' in query:
            open_cmd()
            
        elif 'open camera' in query:
            open_camera()
        
        elif 'ip address' in query:
                ip_address = find_my_ip()
                speak(f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
                print(f'Your IP Address is {ip_address}')
            
        elif 'work on youtube' in query:
            speak('What do you want to play on Youtube, sir?')
            video = takeCommand().lower()
            play_on_youtube(video)

        elif 'search on google' in query:
            speak('What do you want to search on Google, sir?')
            query = takeCommand().lower()
            search_on_google(query)

        elif "send a whatsapp message" in query:
            speak(
                'On what number should I send the message sir? Please enter in the console: ')
            number = input("Enter a number:")
            speak("What is the message sir?")
            message = takeCommand().lower()
            send_whatsapp_message(number, message)
            speak("I've sent the message sir.")
            
        elif 'tell me joke' in query:
            speak(f"Hope you like this one sir")
            joke = get_random_joke()
            speak(joke)
            speak("For your convenience, I am printing it on the screen sir.")
            pprint(joke)

        elif "give an advice" in query:
            speak(f"Here's an advice for you, sir")
            advice = get_random_advice()
            speak(advice)
            speak("For your convenience, I am printing it on the screen sir.")
            pprint(advice)
            
        elif "news update" in query:
            speak(f"I'm reading out the latest news headlines, sir")
            speak(get_latest_news())
            speak("For your convenience, I am printing it on the screen sir.")
            print(*get_latest_news(), sep='\n')
            
        elif "trending movies" in query:
            speak(f"Some of the trending movies are: {get_trending_movies()}")
            speak("For your convenience, I am printing it on the screen sir.")
            print(*get_trending_movies(), sep='\n')
            
        elif 'climate' in query:
            ip_address = find_my_ip()
            city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
            speak(f"Getting weather report for your city {city}")
            weather, temperature, feels_like = get_weather_report(city)
            speak(f"The current temperature is {temperature}, but it feels like {feels_like}")
            speak(f"Also, the weather report talks about {weather}")
            speak("For your convenience, I am printing it on the screen sir.")
            print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")
            
        elif 'restart' in query:
            os.system("shutdown /s /t 5")
            
        elif 'shutdown' in query:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        elif 'take screenshot' in query:
            speak("Sir, please tell me name for this screenshot file")
            name = takeCommand().lower()
            speak("Please sir hold the screen for few seconds, I am taking screenshot")
            time.sleep(5)
            img=pyautogui.screenshot()
            img.save(f"{name}.png")
            speak("I am done sir, the screenshot is in our main floder.")
            
        elif 'open facebook' in query:
            webbrowser.open("www.facebook.com")
            
        elif 'open instagram' in query:
            webbrowser.open("www.instagram.com")
            
        elif 'where i am' in query or 'where we are' in query:
            speak("wait sir, let me check")
            try:
                ipAdd = requests.get('https://api.ipify.org').text
                print(ipAdd)
                url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
                geo_requests = requests.get(url)
                geo_data = geo_requests.json()
                city = geo_data['city']
                country = geo_data['country']
                speak(f" we are in {city} city of {country} country")
            except Exception as e:
                speak("sorry sir,Due to network issues i am not able to find where we are")
            
            
            '''if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia","")
            results = wikipedia.summary(f'{query}', sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)'''