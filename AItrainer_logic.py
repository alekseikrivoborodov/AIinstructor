import cv2
import keyboard
import numpy as np
import time
import PoseModule as pm



def application():
    
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    # cap = cv2.VideoCapture("/videos_for_determine/1kk5ww.gif")
    # cap = cv2.VideoCapture("Зомб.mp4")
    
    
    detector = pm.poseDetector()
    
    count = 0
    dir = 0
    pTime = 0
    
    right_arm_values, left_arm_values = [], []
    
    while not keyboard.is_pressed('q'):
        success, img = cap.read()
        img = cv2.resize(img, (1280, 720))
        # img = cv2.imread("AiTrainer/test.jpg")
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)
        
        
        def determine_exersize_arms():
            cv2.putText(img, "Program training...", 
                        (170, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                                (0, 0, 0), 5)
            
            angle_right_arm = detector.findAngle(img, 12, 14, 16)
            angle_left_arm = detector.findAngle(img, 11, 13, 15)

            if angle_right_arm not in right_arm_values:
                right_arm_values.append(angle_right_arm)
            if angle_left_arm not in left_arm_values:
                left_arm_values.append(angle_left_arm)
            
         
        if len(lmList) != 0:           
            # Training stage
            # for i in range(10):
            #     determine_exersize_arms()
            
            # angle_right_arm = detector.findAngle(img, 12, 14, 16)
            # angle_left_arm = detector.findAngle(img, 11, 13, 15)
            
            angle_right_knee = detector.findAngle(img, 23, 25, 27)
            angle_left_knee = detector.findAngle(img, 24, 26, 28)
            
            # математический расчет
            # per = np.interp(angle_right_arm, (int(min(right_arm_values)), int(0.9*max(right_arm_values))), (0, 100))
            # bar = np.interp(angle_right_arm, (int(min(right_arm_values)), int(0.9*max(right_arm_values))), (650, 100))
            
            
            # гантели
            # per = np.interp(angle_right_arm, (210, 310), (0, 100))
            # bar = np.interp(angle_right_arm, (220, 310), (650, 100))
            
            # отжимания
            # per = np.interp(angle_left_arm, (190, 240), (0, 100))
            # bar = np.interp(angle_left_arm, (190, 240), (650, 100))
            
            # приседания
            per = np.interp(angle_right_knee, (190, 250), (0, 100))
            bar = np.interp(angle_right_knee, (190, 250), (650, 100))
        
            
            # Check for the dumbbell curls
            color = (255, 255, 255)
            if per == 100:
                color = (0, 0, 255)
                if dir == 0:
                    count += 0.5
                    dir = 1
            if per == 0:
                color = (255, 255, 255)
                if dir == 1:
                    count += 0.5
                    dir = 0
            # print(count)

            # Draw Bar
            cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
            cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
            cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                                color, 4)

            # Draw Curl Count
            cv2.rectangle(img, (0, 550), (250, 720), (0, 0, 0), cv2.FILLED)
            cv2.putText(img, str(int(count)), (40, 695), cv2.FONT_HERSHEY_PLAIN, 10,
                                (255, 255, 255), 25)

            # Determine and draw the fps
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                        (0, 0, 0), 5)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
        
        
if __name__ == "__main__":
    application()