# -*- coding: utf-8 -*-
import requests
import cv2
import json
import random
import openpyxl
from moviepy.editor import VideoFileClip
import speech_recognition as sr
import pygame
import pyautogui
import math
try:
    import Image
except ImportError:
    from PIL import Image
screen_id = 0

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
#pygame.init()  #pygame 초기화

#음성인식 함수
def recognize_speech_from_mic(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")
    #마이크 입력
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source,duration=1)
        print ("Say something!")
        audio = recognizer.listen(source)
        print ("end recognition")
	# set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"
    return response

#음성인식 범위 넓혀주는 함수
def selectname(randnumb, response2):
    print("랜덤한 숫자 : "), randnumb
    print("실제로 음성 인식한 내용 : "), response2
    correct = 2

    if (randnumb == 0):
        if response2 in ('navigation', 'vacation', 'delegation', 'randiation', 'navigate', 'Asian', 'dedication', 'definition', 'litigation', 'baby Asian', 'reggaeton', 'meditation', 'vision', 'Nick Cannon'):
            correct = 1
        else:
            correct = 2
    elif (randnumb == 1):
        if response2 in ('happy birthday', 'birthday', 'divorcee', 'North Bay', 'Thursday', 'PRCA', 'Weber State'):
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
            correct = 2
    else:
        print("please say again")
    return correct

#분류된 조건에 따라 영상 랜덤으로 골라주는 함수
def facerecog(facepose, smale, sfemale, max_male, max_female, facegender):
    cell = None
    start = 0
    end = 0
    if facepose=='100' or smale == '100' or sfemale =='100' or max_male =='100' or max_female=='100' or facegender=='100':
        faceposenum = 2
        print ("recognize face error")
    elif facepose == "frontal_face" or "left_face" or "right_face" or "rotate_face" :
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
            break
    return cell, err

while True:
    if framenum == 3:
        framenum = 0
    else:
        framenum = framenum + 1

    #stt이미지 랜덤으로 선택해줌
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
            break
        else:
            ori = frame.copy()  # 나중에 frame 의 원본을 쓰기 위해 ori 에 복사한 것으로 얼굴을 인식시킨다.
            img_gray = cv2.cvtColor(ori, cv2.COLOR_BGR2GRAY)
            cascade_file = "/home/pi/projects/opencv-CFR-advertisement-system-rpi/haarcascade_frontalface_default.xml"  # https://github.com/opencv/opencv/tree/master/data/haarcascades xml파일 다운경로
            cascade = cv2.CascadeClassifier(cascade_file)
            face_list = cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=3, minSize=(50, 50))  # 가까이있는 얼굴만 인식하려면 숫자 올리기

            if len(face_list) > 0:
                print(face_list)
                color = [(0, 0, 255), (0, 255, 0)]
                for face in face_list:
                    x, y, w, h = face
		    # cv2.rectangle(frame, (x, y), (x + w, y + h), color[0], thickness=3) #n번째가 아닌 인식되는 즉시 즉시를 보려면 이 코드 사용
		    # cv2.imshow('video', frame)

                if framenum == 3:  # 실험 결과 세번재 프레임을 사용
                    cv2.rectangle(ori, (x, y), (x + w, y + h), color[0], thickness=3)
                    #cv2.imshow('video', ori)

                    #crop = ori[y + 5:y + h - 5, x + 5:x + w - 5]  # 크롭이미지로 이미지 판별 빨간 줄은 저장하지않도록 선의 굵기만큼 빼고 더한다.
                    #imgpath = ('C:/Users/dbstn/Desktop/nene/cropimg%d.jpg' % (imgnum))

                    crop = frame  # crop 이지만 크롭하지 않은 전체 이미지를 저장해서 CFR이 인식하도록 함. 추후 수정필요
                    imgpath = ('/home/pi/projects/opencv-CFR-advertisement-system-rpi/crop/img%d.png' % (imgnum))

                    imgnum = imgnum + 1
                    cv2.imwrite(imgpath, crop)
                    files = {'image': open(imgpath, 'rb')}

                    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret}
                    response = requests.post(url, files=files, headers=headers)
                    rescode = response.status_code

                    if (rescode == 200):
                        facepose = '100'
                        smale = '100'
                        sfemale = '100'
                        max_male = '100'
                        max_female = '100'
                        facegender = []
                        faceage = []
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
                            #age is over 10
                            if len(faceage[i]) ==5:
                                average_age.append(int(faceage[i][0] + faceage[i][1]) + 2)
                            #age is under 10
                            else:
                                average_age.append(int(faceage[i][0]) + 2)
                            
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
                                    male[8] += 1
                            elif facegender[i] == "female":
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
                                else:
                                    female[8] += 1
                            else:
                                if 1 <= average_age[i] < 10: #child일경우.10대이상부턴 오류이기 때문에  의미로 1이 아닌 조정된 가중치인 0.5를 부여
                                    male[0] += 1
                                elif 10 <= average_age[i] < 20:
                                    male[1] += 0.5
                                    female[1] += 0.5
                                elif 20 <= average_age[i] < 30:
                                    male[2] += 0.5
                                    female[2] += 0.5
                                elif 30 <= average_age[i] < 40:
                                    male[3] += 0.5
                                    female[3] += 0.5			
                                elif 40 <= average_age[i] < 50:
                                    male[4] += 0.5
                                    female[4] += 0.5
                                elif 50 <= average_age[i] < 60:
                                    male[5] += 0.5
                                    female[5] += 0.5
                                elif 60 <= average_age[i] < 70:
                                    male[6] += 0.5
                                    female[6] += 1
                                elif 70 <= average_age[i] < 80:
                                    male[7] += 0.5
                                    female[7] += 0.5
                                else:
                                    male[8] += 0.5
                                    female[8] += 0.5
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
                        #smale = math.ceil(smale)#굳이 정수일 필요가없네
                        sfemale = sum(female)
                        #sfemale = math.ceil(sfemale)
                        sgen = smale + sfemale#한명인데 0.5+0.5=2 나왔었다. ceil때문에
                        print(male, female) # 남 녀 배열
                        print(smale, sfemale) # 남자 수 여자 수
                        print(max_male, max_female) # 성별별로 가장 많은 나이대

                        cel, err = facerecog(facepose, smale, sfemale, max_male, max_female, facegender)

                        if err == 0 :
                            print(cel)
                            cel = cel[:-4]
                            clip1 = VideoFileClip('/home/pi/Downloads/'+cel+'1'+'.mp4')
                            clip2 = VideoFileClip('/home/pi/Downloads/'+cel+'2'+'.mp4')
                            clip1_resized = clip1.resize(height=height-20, width=width)
                            clip2_resized = clip2.resize(height=height-20, width=width)
                            # pygame.display.set_caption('first video!')
                            clip1_resized.preview(fullscreen=True) 
                            # clip1.preview() 
                            pygame.quit()
                            
                            if sgen == 1: #인식된 사람이 한 명일때는 음성인식, stt이미지
                                #p = subprocess.Popen('exec '+'python imviewer.py',stdout=subprocess.PIPE, shell=True)
                                width, height = pyautogui.size()
                                image = cv2.imread('/home/pi/projects/opencv-CFR-advertisement-system-rpi/sst/'+randname+'.jpg')
                                noviceimg = cv2.imread('/home/pi/projects/opencv-CFR-advertisement-system-rpi/sst/again.png')
                                qrimage = cv2.imread('/home/pi/projects/opencv-CFR-advertisement-system-rpi/sst/qrcodefull.png')
                                #cv2.imshow('image',image)
                                #cv2.waitKey(1)
                                print ("발음해야 할 단어 : " + randname)
                                window_name = 'projector'
                                cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
                                cv2.moveWindow(window_name, width, height)
                                cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
                                cv2.imshow(window_name, image)
                                cv2.waitKey(500)

                                while True:
                                    recognizer = sr.Recognizer()
                                    mic = sr.Microphone(device_index=2)
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


                            # pygame.display.set_caption('second video!')
<<<<<<< HEAD
                            clip2_resized.preview(fullscreen=True)
=======
                            clip2_resized.preview(fullscreen=True)  # 작은화면 디버깅시 이용
>>>>>>> 08aa95e91bf50e5175eda61f3638f254cd6c5b0d
                            # clip2.preview(fullscreen=True)
                            pygame.quit()
                            # clip2.close() # clip1.close 등 moviepy 명령어인 close 쓰니깐 느림. 팅기는 현상
                            if sgen == 1:
                                window_name = 'QR'
                                cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
                                cv2.moveWindow(window_name, width, height)
                                cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
                                cv2.imshow(window_name, qrimage)
                                cv2.waitKey(8000)
                                cv2.destroyAllWindows()
                        
                        
                        else :
                            print ("facepose error")
                    else:
                        print("Error Code:" + rescode)
            else:
                print ("no face list")
cap.release()
cv2.destroyAllWindows()
