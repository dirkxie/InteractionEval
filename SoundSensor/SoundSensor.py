import urllib
import time
import mraa
import numpy as np
import sys

soundSensor = mraa.Aio(0)
#soundSensor.dir(mraa.DIR_OUT)

def main():
    while True:
        soundValue = soundSensor.read()
        print soundValue
        time.sleep(0.1)
main()
