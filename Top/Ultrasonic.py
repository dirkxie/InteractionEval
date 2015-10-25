import urllib
import time
import mraa
import numpy as np
import sys

def main():
    trigPin = mraa.Gpio(5)
    trigPin.dir(mraa.DIR_OUT)

    echoPin = mraa.Gpio(4)
    echoPin.dir(mraa.DIR_IN)

    led = mraa.Gpio(8)
    led.dir(mraa.DIR_OUT)
    
    while True:
        trigPin.write(0)
        time.sleep(0.002)
        trigPin.write(1)
        time.sleep(0.01)
        trigPin.write(0)
        
        while echoPin.read() == 0:
            pulseOff = time.time()
        while echoPin.read() == 1:
            pulseOn = time.time()

        timeDiff = pulseOn - pulseOff
        #print timeDiff
        
        distance = timeDiff * 17000;
        #if (distance >= 400 || distance <= 0)
        #    print 'out of range'
        print distance, 'cm'
        time.sleep(0.988)
main()
