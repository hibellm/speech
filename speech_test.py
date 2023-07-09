#!/usr/bin/python3
# -*- encoding: utf-8 -*-

"""
CREATED    :
AUTHOR     :
DESCRIPTION:
"""

# NOTE: this example requires PyAudio because it uses the Microphone class
from find_files import find_filelist
import string
import speech_recognition as sr
from houndify import *
from word2number import w2n
import pygame
import time
import nltk
import os
import pyttsx3

# from nltk.corpus import words, stopwords
# nltk.download('stopwords')
# nltk.download('words')



def yousaidwhat():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # recognize speech using Houndify
    try:
        speech = r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY)
        print(f"Houndify thinks you said: {speech}")
        return speech

    except sr.UnknownValueError:
        print("Houndify could not understand the audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Houndify service: {e}")
        return None


def playme(song, snipit=20):
    # INIT THE MIXER THEN PLAY SONG
    # file = 'N:\William Shatner\Miss Congeniality Soundtrack\Miss Congeniality Soundtrack - 12 - William Shatner - Miss United States (Berman Brother Mix).mp3'
    pygame.init()
    pygame.display.set_mode((200, 100))
    pygame.mixer.init()
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    pygame.event.wait()
    time.sleep(snipit)
    pygame.mixer.music.stop()

def stopme():
    # STOP THE PLAYER
    pygame.mixer.music.stop()



# Process the speech
speech = yousaidwhat()
saywhat(speech)



folderspeech = 'create folder one two three abc'
setupspeech  = ['set up study g o one eight nine eight seven x',
                'set up study g o 1 8 9 8 7 x',
                'anonymize gx zero one two four eight',
                'anonymize g ex oh two three four',
                'anonymize a. b c. d one two three four five',
                'make folder x y z two to two']


speech = 'play songs one'


def saywhat(speech):
    try:
        engine = pyttsx3.init()
    except ImportError as e:
        print('TTS driver not found')
    except RuntimeError as e:
        print('TTS driver failed to initialize')

    rate = engine.getProperty('rate')
    volume = engine.getProperty('volume')
    voices = engine.getProperty('voices')

    engine.setProperty('rate', rate - 50)
    engine.setProperty('volume', volume - 0.25)
    engine.setProperty('voice', voices[0])

    engine.say(speech)
    engine.runAndWait()

saywhat(speech)
saywhat(setupspeech)
saywhat(setupspeech2)

# RUN THROUGH THE DIFFERENT VOICES AVAILABLE
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
   engine.setProperty('voice', voice.id)
   print(voice.id)
   engine.say('The quick brown fox jumped over the lazy dog.')
engine.runAndWait()



def process_speech(speech):
    print(f'Speech is : "{speech}"')

    # CLEAN UP SPEECH
    clean_speech = speech.translate(str.maketrans('', '', string.punctuation))

    # PUT THE SPEECH INTO LIST AND TAG
    tagged = nltk.pos_tag(clean_speech.split(' '))
    tagged[0:]
    print(tagged)

    ptagged = []
    for word in tagged:
        if word[1] == 'CD':
            ptagged.append([w2n.word_to_num(word[0]), word[1]])
        else:
            ptagged.append(word)
    return ptagged

a = process_speech(setupspeech[5])
w = []
for t in a:
    if t[1] in ('VB', 'NN'):
        w.append(t[0]+" ")
    else:
        w.append(str(t[0]))
    x = ''.join(w)

print(f"SO I think the answer is : {x}")

print(w2n.word_to_num(setupspeech[5]))

def getmusic():
    path = 'N:\\'
    mymusic = find_filelist(path, '*.mp3', True)

    return mymusic


def getplaylist():
    # GET MUSIC PLAYLIST
    path = 'N:\\Playlists'
    mymusic = find_filelist(path, '*.m3u', True)

    with open(mymusic[0]) as f:
        content = f.readlines()
    content.pop(0)

    mymusic = []
    for c in content:
        b = c.replace('/', '\\').replace('\n','').replace('..\\', 'N:\\')
        mymusic.append(c)

    return mymusic



def playsongs(speech):
    # GET MUSIC LIST
    mymusic = getmusic()

    track = speech.split(' ')[2:]
    tracknum = w2n.word_to_num(' '.join(track))

    if speech.split(' ')[0] == 'play':
        # PLAY SOME MUSIC
        playme(mymusic[tracknum])
    else:
        print('cant play anything - number too big')


def playlist(speech):
    # GET MUSIC PLAYLIST
    mymusic = getplaylist()

    # track = speech.split(' ')[2:]
    # tracknum = w2n.word_to_num(' '.join(track))

    if speech.split(' ')[0] == 'play':
        # PLAY SOME MUSIC - LOOP
        for i, j in enumerate(mymusic):
            playme(mymusic[i])
    else:
        print('cant play anything - number too big')

speech = yousaidwhat()
speech='play song one'
playlist(speech)


def makefolder():
    speech = yousaidwhat()
    # a = process_speech(setupspeech[5])
    a = process_speech(speech[0])
    w = []
    for t in a:
        if t[1] in ('VB', 'NN'):
            w.append(t[0] + " ")
        else:
            w.append(str(t[0]))
        x = ''.join(w)

    print(f"So I think the answer is : {x}")
    x_clean = [y for y in x.split(' ') if y != '']
    if x_clean[0] in ['folder', 'make']:
        if not os.path.isdir(os.path.join('.', x_clean[-1])):
            os.makedirs(os.path.join('.', x_clean[-1]))
    elif x_clean[0] in ['play']:
           playme(mymusic[20])
    elif x_clean[0] in ['anonymize']:
        print(f"I would have anonymized study: {x_clean[-1]}")
    else:
        print(f"No idea what to do with:  {x}")

makefolder()