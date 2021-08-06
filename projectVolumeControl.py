#########################################################################################


#Importing Dependencies
import cv2
import mediapipe as mp
import time
import math
import numpy as np
import HandTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


###########################################################################################



cap = cv2.VideoCapture(0)
wCam, hCam = 640,480            #Setting size of the camera screen
cap.set(3, wCam)
cap.set(4, hCam)


#########################################################################################


cTime = 0
pTime = 0

detector = htm.handDetector(min_detection_confidence = 0.7)



#Using pycaw module to control the volume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]


vol= 0
volBar = 400
volPercentage = 0



#########################################################################################



while True:
    
    success, img = cap.read()
    
    img = detector.findHands(img)
    
    lmList = detector.findPosition(img, draw = False)
    if(len(lmList) !=0):
        #print(lmList[4], lmList[8])
        
        
        #Getting positions of thumb and index finger
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx,cy = (x1+x2)//2, (y1+y2)//2      #Getting center of the line between thumb and index finger
        
        
        cv2.circle(img, (x1,y1), 12, (0,255,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 12, (0,255,255),cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (225,225,0))
        cv2.circle(img, (cx,cy), 12, (0,255,255),cv2.FILLED)
       
        length = math.hypot(x2-x1,y2-y1)
        #print(length)
        
        vol= np.interp(length,[25, 185], [minVol,maxVol])
        volBar= np.interp(length,[25, 185], [400,150])
        volPercentage= np.interp(length,[25, 185], [0,100])
        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)
        
        
        
        if length<30:
            cv2.circle(img, (cx,cy), 12, (225,0,0),cv2.FILLED)
        if length>185:
            cv2.circle(img, (cx,cy), 12, (225,0,255),cv2.FILLED)
            
        
        #max len = 185
        #min len = 25
        #handRange = 25 - 185
        #vol Range = -65 - 0
        
    #Setting the Volume bar and percentage
    cv2.rectangle(img, (50,150), (85,400), (255,0,0))
    cv2.rectangle(img, (50, int(volBar)), (85,400), (255,0,0), cv2.FILLED)
    cv2.putText(img, f'{int(volPercentage)} %', (10,450), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0),2)
    
    
    
    #For Displaying FPS on Camera screen        
    cTime=time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    
    
    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0),2)
    
    
    
    
    
    
    cv2.imshow("Image", img)
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
    
    