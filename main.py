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

from concurrent.futures import ThreadPoolExecutor

    
MOVE_X = 100

class App:

    def __init__(self):

        # get my API key of ChatGPT from the environment variable
        api_key = os.environ['CHAT_GPT_API_KEY']
        openai.api_key = api_key

        self.mic = sr.Microphone()
        self.recognizer = sr.Recognizer()

        self.questions = []
        self.recognition_lang = "ja-JP"

        self.replys = False

        self.TRIGGER = "せいさん"
        self.MAX_COMMENT_SIZE = 130

    def run(self):

        # start with multi threads
        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(self.listen_voice)
            executor.submit(self.recognize_voice)
    
    def listen_voice(self):
        while True:
            with self.mic as source:
                # input sound through mic
                audio = self.recognizer.listen(source)
        
            self.questions.append(audio)
            print("Questions = " + str(len(self.questions)))

    def recognize_voice(self) -> str:
        while True:
            if len(self.questions) > 0:
                audio = self.questions.pop(0)

                # recognize speech using Google Speech Recognition
                try:
                    recognized_text = self.recognizer.recognize_google(audio, language=self.recognition_lang)
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    pass
                else:
                    print(recognized_text)

                    if "please recognize japanese" in recognized_text.lower():
                        self.recognition_lang = 'ja-JP'
                        self.comment("日本語を認識します")
                    elif "英語を認識してください" in recognized_text:
                        self.recognition_lang = 'en-US'
                        self.comment("Now I'm recognizing English.")
                    #elif "中国語を認識してください" in recognized_text:
                    #    self.recognition_lang = 'cmn-Hans-CN'
                    elif recognized_text == self.TRIGGER:
                        self.replys = True

                    elif self.TRIGGER in recognized_text or self.replys:
                        answer = self.get_reply_from_chatpgt(recognized_text)

                        split_answer = [answer[i:i+self.MAX_COMMENT_SIZE] for i in range(0, len(answer), self.MAX_COMMENT_SIZE)]

                        for ans in split_answer:
                            self.comment(ans)

                        self.replys = False

            time.sleep(0.3)


    def comment(self, text):
        # copy to the clipboard
        pyperclip.copy(text)

        # input the comment
        self.move_to_input()
        pyautogui.hotkey("command", "v")

        time.sleep(0.5)

        # send the comment
        self.move_to_send()
        pyautogui.click()

        time.sleep(1)

    def comment_chatgpt(self):
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
    
    def get_reply_from_chatpgt(self, question):
        print("before gpt")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "user", "content": question},
        ],)
        str = response.choices[0]["message"]["content"].strip()
        print("get ans")

        return str
        
    def move_to_send(self):
        pyautogui.move(MOVE_X, 0)

    def move_to_input(self):
        pyautogui.move(-MOVE_X, 0)

if __name__ == '__main__':
    App().run()
