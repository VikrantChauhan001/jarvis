#importing the required libraries
import speech_recognition as sr
from time import ctime
import time
import datetime
from bs4 import BeautifulSoup
import requests
import webbrowser
import os
from pydub import AudioSegment
from pydub.playback import play
import random
from playsound import playsound
from gtts import gTTS

#this function lets the jarvis speak
def speak(audioString):
    tts = gTTS(text=audioString, lang='en')
    tts.save("audio.mp3")
    audio = AudioSegment.from_mp3("audio.mp3")
    print(audioString)
    play(audio)

#this function records the command and converts it to text using gTTS
def recordAudio():
    r = sr.Recognizer()
    with sr.Microphone(device_index = 1) as source:
        print("Listening...")
        audio = r.listen(source)

    data = ""
    try:  
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return data


# This function performs all the tasks
def jarvis(data):
    if "how are you" in data:
        speak("I am fine, thanks for asking")
    if "what can you do" in data:
        speak("I am unperfected right now, but.\nI can tell you the current time.\nI can tell you the temperature in any city.\nI can play you a song.")

    if "what time is it" in data:
        speak(ctime())
    if "play the song" in data:
        song_list = data.split(" ")
        song=""
        for i in range(3,len(song_list)):
            song = song+" "+song_list[i]
        speak("Hold on, I will play"+song)
        html = requests.request("GET","https://www.youtube.com/results?search_query={0}".format(song)).content
        soup = BeautifulSoup(html, "html.parser")
        tag = soup.find("a",{"class":"yt-uix-sessionlink spf-link"})
        video_link = (tag.attrs["href"])
        webbrowser.open("https://www.youtube.com"+video_link)

    if "what is the temperature in" in data:
        data = data.split(" ")
        location = ""
        for i in range(5,len(data)):
            location = location+" "+data[i]
        speak("Hold on, I will show you the temperature in" + location)
        html = requests.request("GET","https://www.google.com/search?q=temperature+in+{0}".format(location)).content
        time.sleep(0.5)
        soup = BeautifulSoup(html, "html.parser")
        speak("The current temperature in "+soup.find("span",{"class":"tAd8D"}).text+ " is: "+soup.find("div",{"class":"BNeawe"}).text)
    if "thank you" in data:
        speak("Glad to help, you're welcome, goodbye")
        exit()

#Calling the jarvis
list_words = ["beautiful","graceful","marvelous","wonderful"]
hour = int(datetime.datetime.now().hour)
if hour>=0 and hour<12:
    speak('Hi vikrant! Good Morning. \nThis is such a '+list_words[random.randint(0,len(list_words)-1)]+' day today. What can i do for you?')
 
elif hour>=12 and hour<18:
    speak('Hi Vikrant, Good Afternoon.\nThis is such a '+list_words[random.randint(0,len(list_words)-1)]+' day today. What can i do for you?')
 
else:
    speak('Hello Vikrant, Good Evening.\nThis is such a '+list_words[random.randint(0,len(list_words)-1)]+' day today. What can i do for you?')
print("Start by asking 'what can you do?'")
while 1:
    data = recordAudio()
    jarvis(data)
