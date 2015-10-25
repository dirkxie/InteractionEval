import urllib
import time
import mraa
import numpy as np
import sys

def main():
    soundSensor = mraa.Aio(0)
    while True:
        soundValue = soundSensor.read()
        print soundValue
        time.sleep(0.1)
main()
