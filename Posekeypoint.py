import cv2
import mediapipe as mp
import time
mp_drawing = mp.solutions.drawing_utils          # mediapipe 繪圖方法
mp_drawing_styles = mp.solutions.drawing_styles  # mediapipe 繪圖樣式
mp_pose = mp.solutions.pose                      # mediapipe 姿態偵測

cap = cv2.VideoCapture(0)  # webcam
pTime = 0

# 啟用姿勢偵測
with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:

    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    lmList = []
    while True:
        ret, img = cap.read()
        if not ret:
            print("Cannot receive frame")
            break
        img = cv2.resize(img, (520, 300))             # 縮小尺寸，加快演算速度
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # 將 BGR 轉換成 RGB
        results = pose.process(img2)                  # 取得姿勢偵測結果

        # print(results.pose_landmarks)
        # 根據姿勢偵測結果，標記身體節點和骨架
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            for index, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)

            # 列印姿態關鍵點坐標，返回x,y,z,visibility
            #print(index, cx, cy)

            # 保存坐標信息
            lmList.append((cx, cy))

            # 在關鍵點上畫圓圈，img畫板，以(cx,cy)為圓心，半徑5，顏色綠色，填充圓圈
            cv2.circle(img, (cx, cy), 3, (0, 255, 0), cv2.FILLED)
        # 查看FPS
        cTime = time.time()  # 處理完一幀的時間
        fps = 1/(cTime-pTime)
        pTime = cTime  # 重置起始時間

        # 在畫面上顯示fps，先轉換成整數再變成字符串形式，文本顯示坐標，文本字體，文本大小
        cv2.putText(img, str(int(fps)), (70, 50),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        for element in lmList:
            print(element)

        cv2.imshow('image', img)
        if cv2.waitKey(10) & 0xFF == 27:
            break     # 按下 q 鍵停止
cap.release()
cv2.destroyAllWindows()
