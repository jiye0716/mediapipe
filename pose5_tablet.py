import math
import cv2
from time import time
import mediapipe as mp
from pygame import mixer
import tempfile
from gtts import gTTS
import requests

mp_pose = mp.solutions.pose
pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils  

# 計算角度的副函式
def calculateAngle(landmark1, landmark2, landmark3):
    # 獲取所需座標
    x1, y1, _ = landmark1
    x2, y2, _ = landmark2
    x3, y3, _ = landmark3
    # 計算三點之間的夾角
    angle = math.floor(math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2)))
    if angle < 0:
        angle += 360
    if angle>180:
        angle=360-angle
    return angle

def speak(sentence, lang):
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts=gTTS(text=sentence, lang=lang)
        tts.save('{}.mp3'.format(fp.name))
        mixer.init()
        mixer.music.load('{}.mp3'.format(fp.name))
        mixer.music.play(1)

def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
    image.flags.writeable = False                  # Image is no longer writeable
    results = model.process(image)                 # Make prediction
    image.flags.writeable = True                   # Image is now writeable 
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) 
    height, width, _ = image.shape
    landmarks = []
    if results.pose_landmarks:
            # 畫關鍵點在圖片上
        mp_drawing.draw_landmarks(image=image, landmark_list=results.pose_landmarks,
                    connections=mp_pose.POSE_CONNECTIONS)
        for landmark in results.pose_landmarks.landmark:
        # 將關鍵點加進list內.
            landmarks.append((int(landmark.x * width), int(landmark.y * height),
                    (landmark.z * width)))    
    try:
        l_elbow = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])
    except:
        l_elbow=0
    try:
        # 取得右肩、右肘和右腕之間的夾角。    # 12 14 16 
        r_elbow = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])
    except:
        r_elbow=0
    try:
        # 取得左肘、左肩和左臀之間的夾角。    # 13 11 23
        l_shoulder = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])
    except:
        l_shoulder=0
    try:
        # 取得右臀、右肩和右肘之間的夾角。    # 14 12 24
        r_shoulder = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                    landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                    landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])
    except:
        r_shoulder=0
    try: # 左臀角度 
        l_hip = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value])       
    except:
        l_hip=0
    try: # 右臀角度
        r_hip = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value])           
    except:
        r_hip=0
    try:
        # 取得左臀、左膝蓋和左腳踝之間的角度。# 23 25 27
        l_knee = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])
    except:
        l_knee=0        
    try:
        # 取得右臀、右膝蓋和右腳踝之間的角度。# 24 26 28 
        r_knee = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])
    except:
        r_knee=0
    
    return landmarks,image,l_elbow,r_elbow,l_shoulder,r_shoulder,l_hip,r_hip,l_knee,r_knee


url = "http://192.168.0.224:80"
lastTime1 = time()
lastTime2 = time()
cap = cv2.VideoCapture("yoga-1.mp4")  # 開啟鏡頭
with mp_pose.Pose(static_image_mode=False, 
                  min_detection_confidence=0.5,
                  min_tracking_confidence=0.5, 
                  model_complexity=0)as pose:

    while cap.isOpened():
        # Read feed
        ret, frame = cap.read()
        landmarks,output_image,l_elbow,r_elbow,l_shoulder,r_shoulder,l_hip,r_hip,l_knee,r_knee=mediapipe_detection(frame, pose)

        condA = l_shoulder>100 or r_shoulder>100
        condB = l_hip <150 or r_hip <150  

        if condA and (time()-lastTime1)<4:
            text1= 'Shoulders come directly over wrists'
            cv2.putText(output_image, text1, (30, 30),cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2)
        elif condA and (time()-lastTime1)>=4 :
            text1= 'Shoulders come directly over wrists'
            cv2.putText(output_image, text1, (30, 30),cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2)
            speak("肩膀來到手腕的正上方",'zh-tw')
            data = {'shoulder': '1'}
            response = requests.post(url, data=data)
            print(response.text)
            lastTime1 = time()
        else:    
            text1= ' '
            cv2.putText(output_image, text1, (30, 30),cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2)
            if condB and (time()-lastTime2)<5 :
                text2= 'hip and leg straight'
                cv2.putText(output_image, text2, (30, 60),cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2)
            elif condB and (time()-lastTime2)>5 :
                text2= 'ship and leg straight'
                cv2.putText(output_image, text2, (30, 60),cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2)
                speak("臀部與膝蓋打平",'zh-tw')
                data = {'hip':'1','knee': '1'}
                response = requests.post(url, data=data)
                print(response.text)
                lastTime2 = time() 
            else:
                text2= ' success '
                cv2.putText(output_image, text2, (30, 60),cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2)
        color=(0,0,255)
        # try:
        #     cv2.putText(
        #             output_image,
        #             str(l_elbow),
        #             (
        #                 landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value][0],
        #                 landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value][1],
        #             ),
        #             cv2.FONT_HERSHEY_SIMPLEX,
        #             1,color,2,cv2.LINE_AA,)
        # except:
        #     pass
        try:
            cv2.putText(
                    output_image,
                    str(r_elbow),
                    (
                        landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value][0],
                        landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value][1],
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,color,2,cv2.LINE_AA,)
        except:
            pass
        # try:
        #     cv2.putText(
        #             output_image,
        #             str(l_shoulder),
        #             (
        #                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value][0],
        #                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value][1],
        #             ),
        #             cv2.FONT_HERSHEY_SIMPLEX,
        #             1,color,2,cv2.LINE_AA,)
        # except:
        #     pass
        try:
            cv2.putText(
                    output_image,
                    str(r_shoulder),
                    (
                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][0],
                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][1],
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,color,2,cv2.LINE_AA,)
        except:
            pass
        # try:
        #     cv2.putText(
        #             output_image,
        #             str(l_hip),
        #             (
        #                 landmarks[mp_pose.PoseLandmark.LEFT_HIP.value][0],
        #                 landmarks[mp_pose.PoseLandmark.LEFT_HIP.value][1],
        #             ),
        #             cv2.FONT_HERSHEY_SIMPLEX,
        #             1,color,2,cv2.LINE_AA,)
        # except:
        #     pass
        try:
            cv2.putText(
                    output_image,
                    str(r_hip),
                    (
                        landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value][0],
                        landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value][1],
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,color,2,cv2.LINE_AA,)
        except:
            pass
        # try:
        #     cv2.putText(
        #             output_image,
        #             str(l_knee),
        #             (
        #                 landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value][0],
        #                 landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value][1],
        #             ),
        #             cv2.FONT_HERSHEY_SIMPLEX,
        #             1,color,2,cv2.LINE_AA,)
        # except:
        #     pass
        try:
            cv2.putText(
                    output_image,
                    str(r_knee),
                    (
                        landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value][0],
                        landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value][1],
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,color,2,cv2.LINE_AA,)
        except:
            pass



        cv2.imshow('OpenCV Feed', output_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
    cap.release()
    cv2.destroyAllWindows()



