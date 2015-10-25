import sys
import cv2
import urllib
import time
import numpy as np
import mraa

def getFrame(Camera_IP):
        imageFile = urllib.URLopener()
        imageFile.retrieve("http://"+ Camera_IP + ":8080/shot.jpg", 'shot.jpg')

def FaceDetect(face_cascade, flag):
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
def Ultrasonic(trigPin, echoPin):
    trigPin.write(0)
    time.sleep(0.002)
    trigPin.write(1)
    time.sleep(0.01)
    trigPin.write(0)
    
    #read echo time 
    while echoPin.read() == 0:
        pulseOff = time.time()
    while echoPin.read() == 1:
        pulseOn = time.time()
    timeDiff = pulseOn - pulseOff
    #print distance
    distance = timeDiff * 17000
    #if (distance >= 400 || distance <= 0)
    #    print 'out of range'
    #else: 
    print 'distance = ', distance, 'cm'
    time.sleep(0.988)

def SoundSensor(sum, soundSensor):
    for x in range(1,101):
        soundValue = soundSensor.read()
        sum += soundValue
        #print soundValue, 'sum ', sum
    avgSound = sum/100
    print 'avg sound ', avgSound
    time.sleep(0.01)

def main():
    
    ###initialization
    #  IP input, classifier import for face detection  
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    camIP = raw_input("Insert your android camera's IP: ") 
    #  mraa pin assignment
    trigPin = mraa.Gpio(5)      #trigPin for Ultrasonic
    trigPin.dir(mraa.DIR_OUT)   
    echoPin = mraa.Gpio(4)      #echoPin for Ultrasonic
    echoPin.dir(mraa.DIR_IN)
    soundSensor = mraa.Aio(0)   #Analog io for sound sensor
    soundSum = 0

    ###main loop
    while (True):
        #1. face detection
        flag = 0          
        #IP disconnected exception
        try:
            getFrame(camIP)
        except Exception:
            flag = 1
            #time.sleep(1)
            sys.exc_clear()
        #Haar classifier calling 
        FaceDetect(face_cascade, flag)
    
        #2. Ultrasonic distance
        Ultrasonic(trigPin, echoPin)          

        #3. Sound sensor
        soundSum -= 33
        SoundSensor(soundSum, soundSensor)

        #breaking line
        print '==================='
main()
