# zm.py
# Detecte la présence d'utilisateur sur ZM
# 2018-05-03	PV

import socket
import os
import datetime
import time
import random

def ZM_User_Connect_Status(name):
	try:
		print("Get home page", end="", flush=True)
		cmd = 'curl -s http://zambianmeat.com/forum/index.php|grep -q "'+name+'"'
		#print("\r"+cmd)
		response = os.system(cmd)
		#print("\r"+str(response))
		print("\r             \r", end="", flush=True)
		return True if response==0 else False
	except socket.error:
		return False

def trace(s):
	msg = str(datetime.datetime.now())+"\t"+s
	print(msg)
	with open("trace.txt", "a") as myfile:
		print(msg, file=myfile)

lastr = -1
diffCount = 0
downCount = 0
user = "spy18"
os.system("clear;setfont Uni3-Terminus28x14")

try:
	trace("Start watching")  # "+user+" on ZM")
	while True:
		r = ZM_User_Connect_Status(user)
		if r!=lastr:
			lastr = r
			if r:
				trace("\x1b[31;47m True \x1b[37;40m")
			else:
				trace("False")
		time.sleep(random.randint(13,26))

except KeyboardInterrupt:
	os.system("setfont Uni3-Fixed16")
	print("Terminated.")
