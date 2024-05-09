import pickle5 as pickle
import serial
import string
#Originally import datetime.
#import datetime
from datetime import datetime
import os
from threading import Event
from pymavlink import mavutil
import time

#Print information about the process.
print("The print process has the following ID: ")
print(os.getpid())
printEnabled=True
print("Running")
master = mavutil.mavlink_connection('tcp:127.0.0.1:5777') #Open connection for GPS updates.

#Serial configurations.
if(os.environ.get("printEnabled")=="0"):
	print("Serial printing variable is currently disabled.")
ser = serial.Serial('/dev/ttyS0',115200)

#Open the backup file for redundancy.
day = datetime.now()
fileName= "/usr/blueos/userdata/GPSLOGS/" + str(datetime.date(day))+".txt"
textBackup = open(fileName, "a")

values = range(60) #Just a list from 0->60
while(1):
	#if(os.environ.get("printEnabled")=="1"):
	if(printEnabled == True):
		#Originally datetime.datetime.now
		e = datetime.now()
		GPSData = master.recv_match(type='GPS_RAW_INT', blocking = False)
		messageString ="$"+str(time.time()) +"/"+ str(GPSData).replace(" ","")+"\n"
		string2 = messageString.replace(" ","")
		#print(string2)
		ser.write(bytes(messageString,'utf-8')) #Using pickle here to convert the GPSData string to a bytearray for serial printing.
		ser.write(bytes(str('\n'),'utf-8'))
		#Write contents to the backup textfile.
		textBackup.write(messageString)
		textBackup.write("\n")
		Event().wait(1) #Wait one second.
ser.close()
