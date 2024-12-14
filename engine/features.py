import struct
import webbrowser
from hugchat import hugchat
from playsound import *
import eel
import pvporcupine
import pyaudio
from engine.command import *
from engine.config import*
import os
import pywhatkit as kit
import re
import sqlite3

from engine.helper import extract_yt_term
# from engine.db import cursor

conn = sqlite3.connect("lilly.db")
cursor = conn.cursor()

@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\strt_sound.mp3"
    playsound(music_dir)

def openCommand(query):
    query = query.replace(ASSISTANT_NAME,"")
    query = query.replace("open","")
    query.lower()

    app_name = query.strip()

    if app_name != "":
        try:
            # Execute query to search in sys_command table
            cursor.execute(
                'SELECT path FROM sys_command WHERE name = ?', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening " + query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                # If not found in sys_command, check web_command table
                cursor.execute(
                    'SELECT url FROM web_command WHERE name = ?', (app_name,))
                results = cursor.fetchall()

                if len(results) != 0:
                    speak("Opening " + query)
                    webbrowser.open(results[0][0])

                else:
                    # Attempt to run it as a system command or search
                    speak("Opening " + query)
                    try:
                        os.system('start ' + query)
                    except Exception as e:
                        speak("Error: Could not open command or application.")
                        print(f"System command error: {e}")

        except sqlite3.DatabaseError as db_err:
            speak("Database error occurred.")
            print(f"Database error details: {db_err}")
        except Exception as e:
            speak("Something went wrong")
            print(f"General error: {e}")



    # if query!="":
    #     speak("Opening "+query)
    #     os.system('start '+query)
    # else:
    #     speak("not found")

def playYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+ search_term+" on YouTube")
    kit.playonyt(search_term)

def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        porcupine = pvporcupine.create(keywords=["jarvis","alexa"])
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)

        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h"*porcupine.frame_length,keyword)

            keyword_index = porcupine.process(keyword)

            if keyword_index>=0:
                print("hotword detected")
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")

    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response = chatbot.chat(user_input)
    print(response)
    speak(response)
    return response

