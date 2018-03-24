## NetWatcher.py
## Surveille les coupures réseau
## 2016-06-02	PC

import socket
import os
import datetime
import time

def resolve_name(host):
	try:
		#socket.gethostbyname(host)
		#socket.getaddrinfo(host, 80)
		response = os.system("ping -c 1 "+host+" >/dev/null 2>&1")
		return True if response==0 else False
	except socket.error:
		return False

lastr = -1
diffCount = 0
downCount = 0

try:
	while True:
		r = resolve_name("www.google.com")
		if r==lastr:
			diffCount = 0
		else:
			diffCount += 1
			if diffCount==3:
				lastr = r
				diffCOunt = 0
				dt = datetime.datetime.now()
				if r:
					print(str(dt)+"\tUp")
				else:
					downCount+=1
					print(str(dt)+"\tDown", downCount)
		time.sleep(1)

except KeyboardInterrupt:
	print("Terminated.")
