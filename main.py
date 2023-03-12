import pyautogui
import pyperclip
import time
from translate import Translator
import random
import openai
import os
import pyttsx3
import pyaudio
import speech_recognition as sr

    
MOVE_X = 100

class App:

    def __init__(self):
        api_key = os.environ['CHAT_GPT_API_KEY']
        openai.api_key = api_key

        self.r = sr.Recognizer()
        self.mic = sr.Microphone()

    def run(self):
        audio = self.listen_voice()
        text = self.recognize_voice(audio)
        print(text)


    def listen_voice(self):
        with self.mic as source:
            # マイク入力
            audio = self.r.listen(source)
        
        return audio

    def recognize_voice(self, audio) -> str:
        text = ""
        # recognize speech using Google Speech Recognition
        try:
            text = self.r.recognize_google(audio, language='ja-JP')
        except sr.UnknownValueError:
            text = "Unknown Error"
        except sr.RequestError as e:
            text = "Request Error"

        return text

    def comment(self):
        time.sleep(10)
        
        while(True):
            # get a message from ChatGPT
            question = "Name five popular actors in US."
            str = self.get_reply_from_chatpgt(question)

            # copy to the clipboard
            pyperclip.copy(str)

            # input the comment
            self.move_to_input()
            pyautogui.hotkey("command", "v")

            time.sleep(1)

            # send the comment
            self.move_to_send()
            pyautogui.click()

            time.sleep(7)
    
    def get_reply_from_chatpgt(question):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "user", "content": question},
        ],)
        str = response.choices[0]["message"]["content"].strip()
        
    def move_to_send(self):
        pyautogui.move(MOVE_X, 0)

    def move_to_input(self):
        pyautogui.move(-MOVE_X, 0)

if __name__ == '__main__':
    App().run()
