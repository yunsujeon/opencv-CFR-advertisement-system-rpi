# -*- coding: utf-8 -*-
# import time
# import numpy as np
# import moviepy
# from moviepy.editor import *
# from moviepy.video.fx.resize import resize # 이런식으로 가져오면 시간을 줄일 수 있음
# from pygame.locals import *
import requests
import cv2
import json
import random
import openpyxl
from moviepy.editor import VideoFileClip
import subprocess
import speech_recognition as sr
import pygame
import pyautogui

try:
    import Image
except ImportError:
    from PIL import Image

# excel 받아오기
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
print(width)
print(height)
pygame.init()  # 라이브러리 초기화 안해줘도 되긴함


def recognize_speech_from_mic(recognizer, microphone):
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")
# adjust the recognizer sensitivity to ambient noise and record audio
# from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source,duration=1)
        print ("Say something!")
        audio = recognizer.listen(source)

	# set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

# try recognizing the speech in the recording
# if a RequestError or UnknownValueError exception is caught,
#     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"
    return response


def facerecog(facepose, smale, sfemale, max_male, max_female, facegender):
    cell = None
    start = 0
    end = 0
    if facepose == "frontal_face" or "left_face" or "right_face" or "rotate_face" : #여러명일때 facepose는 좀 이상한 감이 있지만..
        faceposenum = 1
        if smale > sfemale :
            if max_male == 0:
                selectnum = 21
                start = 3
                end = 27
            elif max_male ==1:
                selectnum = 22
                start = 3
                end = 27
            elif max_male ==2:
                selectnum = 23
                start = 3
                end = 27
            elif max_male == 3:
                selectnum = 24
                start = 3
                end = 27
            elif max_male == 4:
                selectnum = 25
                start = 3
                end = 27
            elif max_male == 5:
                selectnum = 26
                start = 3
                end = 27
            elif max_male == 6:
                selectnum = 27
                start = 3
                end = 27
            elif max_male == 7:
                selectnum = 28
                start = 3
                end = 27
        elif smale <= sfemale :
            if max_female == 0:
                selectnum = 21
                start = 3
                end = 62
            elif max_female ==1:
                selectnum = 22
                start = 36
                end = 62
            elif max_female ==2:
                selectnum = 23
                start = 3
                end = 62
            elif max_female == 3:
                selectnum = 24
                start = 3
                end = 62
            elif max_female == 4:
                selectnum = 25
                start = 3
                end = 62
            elif max_female == 5:
                selectnum = 26
                start = 3
                end = 62
            elif max_female == 6:
                selectnum = 27
                start = 3
                end = 62
            elif max_female == 7:
                selectnum = 28
                start = 3
                end = 62

    else: #facepose 가 이상할경우
        faceposenum = 2

    while cell is None:
        if faceposenum == 1:
            print(start)
            print(end)
            if start <= end:
                manrownum = random.randrange(start, end)
            else :
                manrownum = random.randrange(end, start)
            print(manrownum, selectnum)
            cell = sheet.cell(row=manrownum, column=selectnum).value
            err = 0
        else:
            cell = None
            err = 1
    return cell, err

while True:
    if framenum == 2:
        framenum = 0
    else:
        framenum = framenum + 1
    ret, frame = cap.read()
    if ret:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        else:
            ori = frame.copy()  # 나중에 frame 의 원본을 쓰기 위해 ori 에 복사한 것으로 얼굴을 인식시킨다.
            img_gray = cv2.cvtColor(ori, cv2.COLOR_BGR2GRAY)
            cascade_file = "/home/pi/projects/opencv-CFR-advertisement-system-rpi/haarcascade_frontalface_default.xml"  # https://github.com/opencv/opencv/tree/master/data/haarcascades xml파일 다운경로
            cascade = cv2.CascadeClassifier(cascade_file)
            face_list = cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=3, minSize=(50, 50))  # 가까이있는 얼굴 인식하고싶어서 150으로 올려둠 멀리있는 얼굴 인식하려면 낮추기

            if len(face_list) > 0:  # face가 없을때도 코드가 돌아야 되는데... 뒤에 else 문 채워주기
                print(face_list)
                color = [(0, 0, 255), (0, 255, 0)]
                for face in face_list:
                    x, y, w, h = face
				# cv2.rectangle(frame, (x, y), (x + w, y + h), color[0], thickness=3) #n번째가 아닌 인식되는 즉시 즉시를 보려면 이 코드 사용
				# cv2.imshow('video', frame)

                if framenum == 2:  # 처음 얼굴을 인식했을 때 말고 시간이 약간 지난 후의 x 번째 프레임을 캡쳐한다.
                    cv2.rectangle(ori, (x, y), (x + w, y + h), color[0], thickness=3)
                    cv2.imshow('video', ori)

                    #crop = ori[y + 5:y + h - 5, x + 5:x + w - 5]  # 크롭이미지로 이미지 판별 빨간 줄은 저장하지않도록 선의 굵기만큼 빼고 더한다.
                    #imgpath = ('C:/Users/dbstn/Desktop/nene/cropimg%d.jpg' % (imgnum))

                    crop = frame  # crop 이지만 크롭하지 않은 전체 이미지를 저장해서 CFR이 인식하도록 함. 추후 수정필요
                    imgpath = ('/home/pi/projects/opencv-CFR-advertisement-system-rpi/crop/img%d.png' % (imgnum))

                    imgnum = imgnum + 1
                    cv2.imwrite(imgpath, crop)
                    files = {'image': open(imgpath, 'rb')}
					# 파일을 저장하지 않고 바로 쓸수는 없는지 생각해보기 files = frame 으로 하면 안되더라.

                    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret}
                    response = requests.post(url, files=files, headers=headers)
                    rescode = response.status_code

                    facegender = []
                    faceage = []

                    if (rescode == 200):
                        print(response.text)
                        data = json.loads(response.text)  # https://developers.naver.com/docs/clova/api/CFR/API_Guide.md#%EC%9D%91%EB%8B%B5-2
                        faceCount = data['info']['faceCount']
                        for i in data['faces']:
                            facepose = i['pose']['value']
                            facegender.append(i['gender']['value'])
                            faceage.append(i['age']['value'])
                            # print("감지된 얼굴의 성별은 {}입니다.".format(facegender))
                            # print("감지된 얼굴의 나이는 {}입니다.".format(faceage))
                            # print("감지된 얼굴의 감정은 {}입니다.".format(faceemo))
                            # print("감지된 얼굴의 방향은 {}입니다.".format(facepose))
                            # print("나이 문자열의 총길이는 {}입니다.".format(agelen))
                            # print("감지된 얼굴의 첫번째 나이대는 {}0대 입니다.".format(firstage))
                            # print("감지된 얼굴의 두번째 나이대는 {}0대 입니다.".format(secondage))

                        average_age = []
                        for i in range(faceCount):
                            average_age.append(int(faceage[i][0] + faceage[i][1]) + 2)
                            print(average_age[i])

                        male = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                        female = [0, 0, 0, 0, 0, 0, 0, 0, 0]

                        for i in range(faceCount):
                            if facegender[i] == "male":
                                if 0 < average_age[i] < 10:
                                    male[0] += 1
                                elif 10 <= average_age[i] < 20:
                                    male[1] += 1
                                elif 20 <= average_age[i] < 30:
                                    male[2] += 1
                                elif 30 <= average_age[i] < 40:
                                    male[3] += 1
                                elif 40 <= average_age[i] < 50:
                                    male[4] += 1
                                elif 50 <= average_age[i] < 60:
                                    male[5] += 1
                                elif 60 <= average_age[i] < 70:
                                    male[6] += 1
                                elif 70 <= average_age[i] < 80:
                                    male[7] += 1
                            else:
                                if 1 <= average_age[i] < 10:
                                    female[0] += 1
                                elif 10 <= average_age[i] < 20:
                                    female[1] += 1
                                elif 20 <= average_age[i] < 30:
                                    female[2] += 1
                                elif 30 <= average_age[i] < 40:
                                    female[3] += 1
                                elif 40 <= average_age[i] < 50:
                                    female[4] += 1
                                elif 50 <= average_age[i] < 60:
                                    female[5] += 1
                                elif 60 <= average_age[i] < 70:
                                    female[6] += 1
                                elif 70 <= average_age[i] < 80:
                                    female[7] += 1

                        max_male = 0
                        max_female = 0
                        for i in range(8):
                            if max(male) != 0:
                                if male[i] == max(male):
                                    max_male = i
                            else:
                                max_male = -1
                            if max(female) != 0:
                                if female[i] == max(female):
                                    max_female = i
                            else:
                                max_female = -1

                        smale = sum(male)
                        sfemale = sum(female)
                        print(male, female) # 남 녀 배열
                        print(smale, sfemale) # 남자 수 여자 수
                        print(max_male, max_female) # 성별별로 가장 많은 나이대

                        cel, err = facerecog(facepose, smale, sfemale, max_male, max_female, facegender)

                        if err == 0 :
                            print(cel)
                            cel = cel[:-4]
                            clip1 = VideoFileClip('/home/pi/Downloads/'+cel+'1'+'.mp4')
                            clip2 = VideoFileClip('/home/pi/Downloads/'+cel+'2'+'.mp4')
                            clip1_resized = clip1.resize(height=height, width=width)
                            clip2_resized = clip1.resize(height=height, width=width)
                            # pygame.display.set_caption('first video!')
                            clip1_resized.preview()  # 작은화면 디버깅시 이용
                            # clip1.preview(fullscreen=True) # 모든화면에서 풀스크린으로 되면 하기 but 팅기더라
                            pygame.quit()
                            p = subprocess.Popen('python imviewer.py', shell=True)
                            while True:
                                recognizer = sr.Recognizer()
                                mic = sr.Microphone(device_index=5)
                                response = recognize_speech_from_mic(recognizer, mic)
                                response2 = response['transcription']
                                if response2 == "snow":  # snow 또는 now 또는 none 등등 예외를 많이 만들어놓기!!! 음성인식 정확도 %의 기준이 될것
                                    print(response2)
                                    p.kill()
                                    break
                                else:
                                    print(response2)

                            # pygame.display.set_caption('second video!')
                            clip2_resized.preview()  # 작은화면 디버깅시 이용
                            # clip2.preview(fullscreen=True)
                            pygame.quit()
                            # clip2.close() # clip1.close 등 moviepy 명령어인 close 쓰니깐 느림. 팅기는 현상
                        else :
                            print ("facepose error")
                    else:
                        print("Error Code:" + rescode)
            else:
                print ("no face list")
cap.release()
cv2.destroyAllWindows()
