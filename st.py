#!/bin/sh
# -*- coding: utf-8 -*-
import requests
import os
import sys
import requests
import cv2
import numpy as np
import json
import subprocess
import speech_recognition as sr
import pygame
from moviepy.editor import VideoFileClip
#from moviepy.editor import *
import pyautogui
import openpyxl
import random
#from moviepy.video.fx.resize import resize
import time
from rand import moviename

try:
    import Image
except ImportError:
    from PIL import Image

imgnum = 0
width, height = pyautogui.size()
print (width)
print (height)
#pygame.init()


def recognize_speech_from_mic(recognizer, microphone):

    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source,duration=1)
        #recognizer.adjust_for_ambient_noise(source)
        print("say something")
        #audio = recognizer.listen(source,timeout=3)
        audio = recognizer.listen(source)
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio, language='en=US')
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

#def recognize_speech_from_mic(audio):
#    try:
#        return r.recognize_google(audio,language='en=US')
#    except sr.UnknownValueError:
#    # except LookupError:
#        print("음성을 말해주세요")
#        return ''

while True:

    clip1 = VideoFileClip('/home/pi/Downloads/adidas1.mp4')
    clip2 = VideoFileClip('/home/pi/Downloads/adidas1.mp4')
    clip1_resized = clip1.resize(height=height-20, width=width)
    clip2_resized = clip1.resize(height=height-20, width=width)
    #pygame.display.set_mode((width,height))
    #pygame.display.set_caption('first video!')
    #clip1_resized.preview()  # 작은화면 디버깅시 이용
    #clip1.preview(fullscreen=True)
    #clip1_resized.close()
    #pygame.quit()
    p = subprocess.Popen('exec '+'python imviewer.py',stdout=subprocess.PIPE,shell=True)
    #p=subprocess.Popen('python imviewer.py',shell=True)
    while True:
        print(moviename)
        recognizer = sr.Recognizer()
        mic = sr.Microphone(device_index=1)# device_index
        response = recognize_speech_from_mic(recognizer, mic)
        response2 = response['transcription']
        print (response)
        if response2 == "bus": 
            print(response2)
            p.kill()
            break
        else:
            print(response2)
                        
    #pygame.display.set_caption('second video!')
    clip2_resized.preview()  # 작은화면 디버깅시 이용
    # clip2.preview(fullscreen=True)
    pygame.quit()
    #clip2_resized.close()
    # clip2.close() # clip1.close 등 moviepy 명령어인 close 쓰니깐 느림. 팅기는 현상
    time.sleep(5)

cap.release()
cv2.destroyAllWindows()



#
# import cv2
# import time
#
# vid = cv2.VideoCapture('C:/Users/dbstn/Desktop/ad/2015oronaminc.mp4') # 재생할 동영상파일
# fps = vid.get(cv2.CAP_PROP_FPS)
# delay = round(1000/fps)/1000 # frame 계산해서 29.7 frame 일 경우 33ms마다 1장 나타나게 했지만 생각보다 딜레이가 더걸림
# while True:
#     ret2, frame2 = vid.read()
#     if ret2:
#         cv2.imshow('ad',frame2)
#         if cv2.waitKey(1) & 0xFF == 27:
#             break
#         time.sleep(delay)
#     else:
#         break
#
# vid.release()
# cv2.destroyAllWindows()

