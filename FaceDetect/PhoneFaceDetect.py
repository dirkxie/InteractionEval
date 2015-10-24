import sys
import cv2
import urllib
import time
import numpy as np
#import mraa

def getFrame(Camera_IP):
        imageFile = urllib.URLopener()
        imageFile.retrieve("http://"+ Camera_IP + ":8080/shot.jpg", 'shot.jpg')
        
def main():
        
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        camIP = raw_input("Insert your android camera's IP: ")
        while(True):
            
            #set flag for exception
            flag = 0
            
            #try except
            try:
                getFrame(camIP) 
            except Exception:
                flag = 1
                time.sleep(1)
                sys.exc_clear()

            #face detection
            if (flag == 1):
                print 'IP Cam disconnected'
            else:
                img = cv2.imread('shot.jpg',0)
                #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                print '====new img===='
                for i in [float(j)/10 for j in range(11,16,1)]:
                        print i
                        faces = face_cascade.detectMultiScale(img, i, 5)
                        #print faces          
                        #faces = face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30,30), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
                        #print faces[0][0]
                        if len(faces)==0:
                                print 'not detected'
                        else:
                                #print faces[0]
                                print faces 
                #time.sleep(1)
main()
