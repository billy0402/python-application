import os
import re

import requests
import speech_recognition  # https://github.com/Uberi/speech_recognition
from bs4 import BeautifulSoup
from gtts import gTTS  # https://github.com/pndurette/gTTS
from hanziconv import HanziConv  # https://github.com/berniey/hanziconv
from pygame import mixer  # https://github.com/pygame/pygame


def bot_listen():
    recognizer = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as microphone:
        audio_data = recognizer.listen(microphone)
    try:
        text = recognizer.recognize_google(audio_data, language='zh-tw')
        return text
    except:
        return '聽不懂'


mixer.init()
if not os.path.exists('temp.mp3'):
    tts = gTTS(text='不重要的語音檔', lang='zh-tw')
    tts.save('temp.mp3')
    print('已產生不重要的語音檔 temp.mp3')


def bot_speak(text, lang):
    try:
        mixer.music.load('temp.mp3')
        gtts = gTTS(text=text, lang=lang)
        gtts.save('speak.mp3')

        mixer.music.load('speak.mp3')
        mixer.music.play()
        while mixer.music.get_busy():
            continue
    except:
        print('播放音檔失敗')


def bot_get_wiki(keyword):
    response = requests.get(f'https://zh.wikipedia.org/zh-tw/{keyword}')
    bs = BeautifulSoup(response.text, 'lxml')
    p_list = bs.find_all('p')
    for p in p_list:
        if keyword in p.text[:len(keyword)]:
            return p.text


def bot_speak_re(sentence):
    sentence = re.sub(r'\[.*?\]', '', sentence)
    print(sentence)
    english_list = re.findall(r'[a-zA-Z ]+', sentence)
    sentence = re.sub(r'[a-zA-Z \-]+', '@English@', sentence)
    all_list = sentence.split('@')

    index = 0
    for text in all_list:
        if text != 'English':
            bot_speak(text, 'zh-tw')
        else:
            bot_speak(english_list[index], 'en')
            index += 1


def bot_get_google(question):
    url = f'https://www.google.com.tw/search?q={question}+site%3Azh.wikipedia.org'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/76.0.3809.100 Safari/537.36'}
    response = requests.get(url, headers=headers)

    if response.status_code == requests.codes.ok:
        soup = BeautifulSoup(response.text, 'lxml')
        wiki_url = soup.find('cite')
        keyword = wiki_url.text.split('/')[-1]
        keyword = HanziConv.toTraditional(keyword)
        return keyword
    else:
        print('請求失敗')
