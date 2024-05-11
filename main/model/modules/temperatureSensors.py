import os
import glob
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/28-'
#device_folder = glob.glob(base_dir + '28*')[0]
outdoorTemp = base_dir + '247f1e1e64ff' + '/w1_slave'
indoorTemp = base_dir + '3e6e1e1e64ff' + '/w1_slave'

class temperatureSensors:

    def  __init__(self):
        return

    def read_temp(self,temp):
        #print(indoorTemp)
        #print(outdoorTemp)
        if temp == 'outdoor':
           lines = self.read_temp_raw(outdoorTemp)
           while lines[0].strip()[-3:] != 'YES':
               time.sleep(0.2)
               lines = self.read_temp_raw(outdoorTemp)
        elif temp == 'indoor':
           lines = self.read_temp_raw(indoorTemp)
           while lines[0].strip()[-3:] != 'YES':
               time.sleep(0.2)
               lines = self.read_temp_raw(indoorTemp)
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c

    def read_temp_raw(self,file):
        f = open(file, 'r')
        lines = f.readlines()
        f.close()
        return lines

