import pyupm_i2clcd as lcd
import mraa
import time
import sys

lcdDisplay = lcd.Jhd1313m1(0, 0x3E, 0x62)
while 1:



        # read pot/print/convert to string/display on lcd
        lcdDisplay.setCursor(0, 0)
        #lcdDisplay.write(potStr)
        lcdDisplay.setColor(0,0,100)
        lcdDisplay.write('23.621345 cm')
        time.sleep(1)


