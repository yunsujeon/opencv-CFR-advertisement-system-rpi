#!/bin/sh
# -*- coding: utf-8 -*-
import requests
import os
import sys
import requests
import cv2
import numpy as np
import json
import speech_recognition as sr
import pygame
from moviepy.editor import VideoFileClip
#from moviepy.editor import *
import pyautogui
import openpyxl
import random
import time
#from moviepy.video.fx.resize import resize
try:
    import Image
except ImportError:
    from PIL import Image

screen_id = 0

#excel 받아오기
excel_document = openpyxl.load_workbook('/home/pi/projects/opencv-CFR-advertisement-system-rpi/data.xlsx')
excel_document.get_sheet_names()
sheet = excel_document.get_sheet_by_name('Sheet1')

cap = cv2.VideoCapture(-1)

client_id = "Nzp_FC__3rbf3tRsbXHR"
client_secret = "eagFGHv7lI"
url = "https://openapi.naver.com/v1/vision/face"  # 얼굴감지
# url = "https://openapi.naver.com/v1/vision/celebrity" # 유명인 얼굴인식

framenum = 0
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
        print("end recognize")    
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

def selectname(randnumb, response2):
    print("랜덤한 숫자 : "), randnumb
    print("실제로 음성 인식한 내용 : "), response2
    #correct = 2
    correct = 1
    """
    if (randnumb == 0):
        if response2 in ('navigation', 'vacation', 'delegation', 'randiation', 'navigate', 'Asian', 'dedication', 'definition', 'litigation', 'baby Asian', 'reggaeton', 'meditation', 'vision', 'Nick Cannon'):
            correct = 1
        else:
            correct = 2
    elif (randnumb == 1):
        if response2 in ('happy birthday.','Pat Metheny', 'happy birthday', 'birthday', 'divorcee', 'North Bay', 'Thursday', 'PRCA', 'Weber State'):
            correct = 1
        else:
            correct = 2
    elif (randnumb == 2):
        if response2 in ('English', 'ego-C', 'ngozi', 'Melissa', 'NBC', 'Embassy', 'Blissey', 'Khaleesi', 'Chrissy', "English C", 'sushi', 'Gracie'):
            correct = 1
        else:
            correct = 2
    elif (randnumb == 3):
        if response2 in ('Museum', 'medium', 'idiom', 'wake me up at', 'video', 'continuum', 'rhenium', 'resume', 'iridium', 'lithium', 'potassium'):
            correct = 1
        else:
            correct = 2
    elif (randnumb == 4):
        if response2 in ('Coca-Cola', 'Aquila', 'koala', 'popular', 'Opera', 'kookaburra', 'Pablo', 'Buffalo'):
            correct = 1
        else:
            correct = 2
    elif (randnumb == 5):
        if response2 in ('Hawaii', 'hi', 'how are you'):
            correct = 1
        else:
           correct = 1
    else:
        print("please say again")"""
    return correct

def facerecog(faceposes, agelens, firstages, facegenders):
    cell= None
    start=0
    end=0
    iagelens = int(agelens)
    ifirstages = int(firstages)
    if faceposes=='100' or agelens =='100' or firstages=='100' or facegenders=='100':
        faceposenum = 2
        print ("recognize face error")
    elif faceposes == "frontal_face"or"rotate_face" or "left_face" or "right_face" :
        faceposenum = 1
        if iagelens is 5:
            if ifirstages is 1:
                if facegenders == ("male"or"child"): #남자10대
                    selectnum = 22
                    start = 3
                    end = 27
                elif facegenders == ("female"or"child"): #여자10대
                    selectnum = 22
                    start = 36
                    end = 62
            elif ifirstages is 2:
                if facegenders == "male": #남자 20대
                    selectnum = 23
                    start = 3
                    end = 27
                elif facegenders == "female": #여자20대
                    selectnum = 23
                    start = 3
                    end = 62
            elif ifirstages is 3:
                if facegenders == "male": #남자30대
                    selectnum = 24
                    start = 3
                    end = 27
                elif facegenders == "female": #여자30대
                    selectnum = 24
                    start = 3
                    end = 62
            elif ifirstages is 4:
                if facegenders == "male": #남자 40대
                    selectnum = 25
                    start = 3
                    end = 27
                elif facegenders == "female": #여자 40대
                    selectnum = 25
                    start = 3
                    end = 62
            elif ifirstages is 5:
                if facegenders == "male": #남자 50대
                    selectnum = 26
                    start = 3
                    end = 27
                elif facegenders == "female": #여자 50대
                    selectnum = 26
                    start = 3
                    end = 62
            elif ifirstages is 6:
                if facegenders == "male": #남자 60대
                    selectnum = 27
                    start = 3
                    end = 27
                elif facegenders == "female": #여자 60대
                    selectnum = 27
                    start = 3
                    end = 62
            elif 6 < ifirstages < 10:
                if facegenders == "male": #남자 70대이상
                    selectnum = 28
                    start = 3
                    end = 27
                elif facegenders == "female": #여자 70대이상
                    selectnum = 28
                    start = 3
                    end = 62
        elif iagelens < 5:
            if -1 < ifirstages < 10:
                if facegenders == ("male"or"child"): #남자 0대
                    selectnum = 21
                    start = 3
                    end = 27
                elif facegenders == ("female"or"child"): #여자 0대
                    selectnum = 21
                    start = 3
                    end = 62
    else:
        faceposenum = 2

    while cell is None:
        if faceposenum ==1:
            print (start)
            print (end)
            if start<=end:
                manrownum = random.randrange(start, end)
            else:
                manrownum = random.randrange(end, start)
            print(manrownum, selectnum)
            cell = sheet.cell(row=manrownum, column=selectnum).value
            err = 0
        else :
            cell = None
            err = 1
            break
    return cell, err

while True:
    if framenum == 3:
        framenum = 0
    else:
        framenum = framenum + 1

    randnumb = random.randrange(0,6)
    if randnumb == 0:
        randname = 'navigation'
    elif randnumb ==1:
        randname = 'happybirthday'
    elif randnumb ==2:
        randname = 'english'
    elif randnumb ==3:
        randname = 'museum'
    elif randnumb ==4:
        randname = 'cocacola'
    elif randnumb ==5:
        randname = 'hawaii'

    ret, frame = cap.read()
    if ret:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            #sys.exit(0)
            break
        else:
            ori = frame.copy()  # 나중에 frame 의 원본을 쓰기 위해 ori 에 복사한 것으로 얼굴을 인식시킨다.
            img_gray = cv2.cvtColor(ori, cv2.COLOR_BGR2GRAY)
            cascade_file = "/home/pi/projects/opencv-CFR-advertisement-system-rpi/haarcascade_frontalface_default.xml"  # https://github.com/opencv/opencv/tree/master/data/haarcascades xml파일 다운경로
            cascade = cv2.CascadeClassifier(cascade_file)
            face_list = cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=3,
                                                 minSize=(50, 50))  # 가까이있는 얼굴 인식하고싶어서 150으로 올려둠 멀리있는 얼굴 인식하려면 낮추기

            if len(face_list) > 0:  # face가 없을때도 코드가 돌아야 되는데... 뒤에 else 문 채워주기
                print(face_list)
                color = [(0, 0, 255), (0, 255, 0)]
                for face in face_list:
                    x, y, w, h = face
                    # cv2.rectangle(frame, (x, y), (x + w, y + h), color[0], thickness=3) #n번째가 아닌 인식되는 즉시 즉시를 보려면 이 코드 사용
                # cv2.imshow('video', frame)

                if framenum == 3:  # 처음 얼굴을 인식했을 때 말고 시간이 약간 지난 후의 x 번째 프레임을 캡쳐한다.
                    cv2.rectangle(ori, (x, y), (x + w, y + h), color[0], thickness=3)
                    #cv2.imshow('video', ori)

                    # crop = ori[y + 3:y + h - 3, x + 3:x + w - 3] #크롭이미지로 이미지 판별 빨간 줄은 저장하지않도록 선의 굵기만큼 빼고 더한다.
                    # imgpath = ('C:/Users/dbstn/Desktop/nene/cropimg%d.jpg' % (imgnum))

                    crop = frame  # crop 이지만 크롭하지 않은 전체 이미지를 저장해서 CFR이 인식하도록 함. 추후 수정필요
                    imgpath = ('/home/pi/projects/opencv-CFR-advertisement-system-rpi/crop/img%d.png' % (imgnum))
                    imgnum = imgnum + 1
                    cv2.imwrite(imgpath, crop)
                    files = {'image': open(imgpath, 'rb')}
# 파일을 저장하지 않고 바로 쓸수는 없는지 생각해보기 files = frame 으로 하면 안되더라.

                    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret}
                    response = requests.post(url, files=files, headers=headers)
                    rescode = response.status_code
                    print("before rescode==200")
                    if (rescode == 200):
                        facepose = '100'
                        firstage = '100'
                        facegender = '100'
                        agelen = '100'
                        print(response.text)
                        data = json.loads(
                            response.text)  # https://developers.naver.com/docs/clova/api/CFR/API_Guide.md#%EC%9D%91%EB%8B%B5-2
                        for i in data['faces']:
                            facegender = i['gender']['value']  # json data의 객체배열을 python으로 출력하고싶음
                            faceage = i['age']['value']
                            faceemo = i['emotion']['value']
                            facepose = i['pose']['value']
                            agelen = len(faceage)  # faceage의 총 길이가 5면 최소 10대 이고 3이면 0~5 4이면 6~10 일 수 있다.
                            firstage = faceage[0]  # faceage의 총 길이에 따라 나이대를 구분한다.
                            secondage = faceage[3]  # 나이대를 정확히 하기 위한 두번 째 변수이다.
                        # print("감지된 얼굴의 성별은 {}입니다.".format(facegender))
                        # print("감지된 얼굴의 나이는 {}입니다.".format(faceage))
                        # print("감지된 얼굴의 감정은 {}입니다.".format(faceemo))
                        # print("감지된 얼굴의 방향은 {}입니다.".format(facepose))
                        # print("나이 문자열의 총길이는 {}입니다.".format(agelen))
                        # print("감지된 얼굴의 첫번째 나이대는 {}0대 입니다.".format(firstage))
                        # print("감지된 얼굴의 두번째 나이대는 {}0대 입니다.".format(secondage))

 # 6번문제. 여기서 문제점 : harsscade에서 얼굴을 인식했는데 그 crop 이미지를 불러왔을때 CFR이 보기에 분석이 불가능하다면 팅김 > 다시 앞으로 돌아가는 알고리즘 필요
                        print (facepose, agelen, firstage, facegender)
                        
                        cel, err = facerecog(facepose, agelen, firstage, facegender)
                        if err ==0 :
                            print (cel)
                            cel = cel[:-4]
                            clip1 = VideoFileClip('/home/pi/Downloads/'+cel+'1'+'.mp4')
                            clip2 = VideoFileClip('/home/pi/Downloads/'+cel+'2'+'.mp4')
                            clip1_resized = clip1.resize(height=height-20, width=width)
                            clip2_resized = clip2.resize(height=height-20, width=width)
                            #pygame.display.set_mode((width,height))
                            #pygame.display.set_caption('first video!')
                            
                            #clip1_resized.preview()  # 작은화면 디버깅시 이용
                            
                            clip1_resized.preview(fullscreen=True)
                            
                            #clip1.preview(fullscreen=True)
                            #clip1_resized.close()
                            pygame.quit()
                            #p = subprocess.Popen('exec '+'python imviewer.py',stdout=subprocess.PIPE,shell=True)
                            width, height = pyautogui.size()
                            novoiceimg = cv2.imread('/home/pi/projects/opencv-CFR-advertisement-system-rpi/sst/again.PNG')
                            image = cv2.imread('/home/pi/projects/opencv-CFR-advertisement-system-rpi/sst/'+randname+'.jpg')
                            #cv2.imshow('image',image)
                            #cv2.waitKey(1)
                            print ("발음해야 할 단어 : " + randname)
                            window_name = 'projector1'
                            cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
                            cv2.moveWindow(window_name, width, height)
                            cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
                            cv2.imshow(window_name, image)
                            cv2.waitKey(500)
                            
                            while True:
                                recognizer = sr.Recognizer()
                                mic = sr.Microphone(device_index=2)# device_index
                                response = recognize_speech_from_mic(recognizer, mic)
                                response2 = response['transcription']
                                correct = selectname(randnumb, response2)
                                print (response)
                                print (response2)
                                print (correct)
                                print("발음해야 할 단어 : " + randname)
                                if correct == 1: 
                                    print response2," >> 변환인식완료 >> ",randname
                                    cv2.destroyAllWindows()
                                    #p.kill()
                                    break
                                else:
                                    print response2," >> 다시 시도해주세요"
                                    cv2.destroyAllWindows()
                                    window_name = 'projector2'
                                    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
                                    cv2.moveWindow(window_name, width, height)
                                    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                                    cv2.imshow(window_name, novoiceimg)
                                    cv2.waitKey(1500)
                                    cv2.destroyAllWindows()
                                    
                                    window_name = 'projector3'
                                    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
                                    cv2.moveWindow(window_name, width, height)
                                    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                                    cv2.imshow(window_name, image)
                                    cv2.waitKey(100)



                            #pygame.display.set_caption('second video!')
                            
                            #clip2_resized.preview()  # 작은화면 디버깅시 이용
                            
                            clip2_resized.preview(fullscreen=True)
                            
                            # clip2.preview(fullscreen=True)
                            pygame.quit()
                            #clip2_resized.close()
                            # clip2.close() # clip1.close 등 moviepy 명령어인 close 쓰니깐 느림. 팅기는 현상
                        else : 
                            print("facepose error")
                    else:
                        print("Error Code:" + rescode)
            else:
                print("no face list")
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

