
import serial
from time import sleep

ser = serial.Serial ("/dev/ttyACM0", 9600)    #Open port with baud rate
while True:
    received_data = ser.read()              #read serial port
    sleep(0.03)
    data_left = ser.inWaiting()             #check for remaining byte
    received_data += ser.read(data_left)
    print (received_data.decode('ascii'))                   #print received data
    ser.write(received_data)                #transmit data serially 
#출처: https://nowprogramming.tistory.com/28 [지금은 프로그래머]