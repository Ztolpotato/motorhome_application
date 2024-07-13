import serial
import time
import string
import pynmea2

class gps:
    #Reads GPS from GPIO15 RXD
    def __init__(self):
        port='/dev/serial0'
        self.ser=serial.Serial(port,baudrate=9600,timeout=0.5)
        dataout =pynmea2.NMEAStreamReader()
    #Reads GPS lat, long and speed. Convert speed in knots to kmh return INT
    def getSpeed(self):
        try: 
          while True:
            newdata=self.ser.readline()
            if (newdata[0:6]).decode() =='$GPRMC':
                newmsg=pynmea2.parse(newdata.decode())
                lat=str(newmsg.latitude)
                long=str(newmsg.longitude)
                speed=str(newmsg.spd_over_grnd)
                if speed != 'None':
                  speed = int((float(speed)*1.85))
                  return speed
                return 'errsig'
            #print("GPS error: decoding gps line is not GPRMC",)
            #return -98
        except Exception as error:
            print("GPS error:", error)
