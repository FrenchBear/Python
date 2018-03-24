# listfiles.py
# Learning Python, getting a list of files
# 2016-06-13	PV

import os
import fnmatch
import re


sdcard = "/home/pi/Pictures/"
includes = ['*.jpg', '*.jpeg']		# Files, case insensitive
excludes = ['*/face_*']				# Files or folders

includes = '|'.join([fnmatch.translate(x) for x in includes])
excludes = '|'.join([fnmatch.translate(x) for x in excludes]) or r'$.'

print("includes: ", includes)
print("excludes: ", excludes)
print()

for root, dirs, files in os.walk(sdcard):
	print("root: ", root)
	print("dirs: ", dirs)
	print("files: ", files)

	files = [os.path.join(root, f) for f in files]
	files = [f  for f in files if not re.match(excludes, f.lower())]
	files = [f  for f in files if re.match(includes, f.lower())]
	print()
	print("selected files: ", files)
	print()


