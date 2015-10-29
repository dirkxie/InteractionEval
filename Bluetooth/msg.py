import serial
ser = serial.Serial("/dev/rfcomm0", timeout=0.5)
ser.write("hello")
ser.read(5)
