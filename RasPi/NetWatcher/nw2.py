# nw.py
# Surveille les coupures réseau
# 2016-06-02	PV

import socket
import os
import datetime
import time

def resolve_name(host):
	try:
		#socket.gethostbyname(host)
		#socket.getaddrinfo(host, 80)
		print("Ping...", end="", flush=True)
		response = os.system("ping -c 1 "+host+" >/dev/null 2>&1")
		print("\r       \r", end="", flush=True)
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

try:
	trace("Start")
	while True:
		r = resolve_name("www.google.com")
		if r==lastr:
			diffCount = 0
		else:
			diffCount += 1
			if diffCount==3:
				lastr = r
				diffCOunt = 0
				if r:
					trace("Up")
				else:
					downCount+=1
					trace("Down {0:d}".format(downCount))
		time.sleep(5)

except KeyboardInterrupt:
	print("Terminated.")
