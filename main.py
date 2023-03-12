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
        api_key = os.environ['CHAT_GPT_API_KEY']
        openai.api_key = api_key

        self.r = sr.Recognizer()
        self.mic = sr.Microphone()

        self.conversation = []

        self.translator = Translator(from_lang = "ja", to_lang = "zh-cn")

    def run(self):

        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(self.listen_voice)
            executor.submit(self.recognize_voice)
    
    def listen_voice(self):
        while True:
            with self.mic as source:
                # マイク入力
                audio = self.r.listen(source)
        
            print("add to conversation")
            self.conversation.append(audio)

    def recognize_voice(self) -> str:
        while True:
            #print("Conversation = ", str(len(self.conversation)))
            if len(self.conversation) > 0:
                audio = self.conversation.pop(0)

                # recognize speech using Google Speech Recognition
                try:
                    text = self.r.recognize_google(audio, language='ja-JP')
                    #text = self.r.recognize_google(audio, language='cmn-Hans-CN')
                    #text = self.r.recognize_google(audio, language='en-US')
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    pass
                else:
                    print(text)
                    print("")
                    #text = self.get_reply_from_chatpgt("この次の文章に対して130字以内で会話のように返答してください。" + text)
                    text = self.get_reply_from_chatpgt("この次の文章に対して簡単に返答してください。" + text)
                    #text = self.translator.translate(text)
                    #print(text)

                    length = len(text)
                    split_text = [text[i:i+130] for i in range(0, length, 130)]

                    for t in split_text:
                        self.comment(t)
                        time.sleep(1)
            
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

        #time.sleep(1)

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
