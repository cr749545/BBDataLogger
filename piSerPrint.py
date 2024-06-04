import pickle5 as pickle
import serial
import string
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
#Open connection to the autopilot.
master = mavutil.mavlink_connection('tcp:127.0.0.1:5777')

#Serial configurations.
if(os.environ.get("printEnabled")=="0"):
	print("Serial printing variable is currently disabled.")
ser = serial.Serial('/dev/ttyS0',115200)

#Open the backup file for redundancy.
day = datetime.now()
fileName= "/usr/blueos/userdata/GPSLOGS/" + str(datetime.date(day))+".txt"
textBackup = open(fileName, "a")

#Start off not loitering.
loitering = False

#Function returns the most recent message of the designated msgType. 
def getMessage(connection, msgType):
	msg = None
	while temp := connection.recv_match(type=msgType):
		msg = temp
	if msg == None:
		msg = connection.recv_match(type=msgType, blocking = True)
	return msg
#Function writes the string to the serial connection (data logger).
def serWrite(serial, msg):
	ser.write(bytes(msg,'utf-8'))
	ser.write(bytes(str('\n'),'utf-8'))

#Main program loop.
while(True):
	#ASection to write GPS information to logger.
	e = datetime.now()
	GPSData = getMessage(master,'GPS_RAW_INT')
	messageString ="$"+str(time.time()) +"/"+ str(GPSData).replace(" ","")+"\n"
	string2 = messageString.replace(" ","")
	serWrite(ser,messageString)
	#Write contents to the backup textfile.
	textBackup.write(messageString)
	textBackup.write("\n")
	time.sleep(1)

	#Section to check when the vehicle is holding position to send START/STOP commands to the PROCV.
	loiterMSG = getMessage(master,'MISSION_CURRENT')
	print("Sequence number:",loiterMSG.seq)
	#Don't want to start in loitering state, so skip over 0.
	#Otherwise, if it even and the vehicle isn't loitering, then set to loiter and turn on PROCV.
	if not loiterMSG.seq==0 and not loitering==True and loiterMSG.seq%2==0 :
		print("Even number detected. Start PROCV.")
		serWrite(ser,"START_PROCV")
		loitering = True
	#If currently loitering and new seq number is even, turn off PROCV.
	elif loitering==True and loiterMSG.seq%2==1:
		print("stoping loitering.")
		serWrite(ser,"STOP_PROCV")
		loitering = False
ser.close()
