#! python
import os
import sys
import subprocess
import re
import glob
import fileinput
import shutil


#define a class of backing up a file, then append a string to the file and finally read the file
class fileappend(object):
	def __init__(self, file, append):
		self.file = file
		self.append = append
	
	def fappend(self):
		f = open(self.file, 'a+')
		print ("appending: ", repr(self.append), self.file)
		f.write(self.append)
		f.seek(0)
		print(f.read())
		f.close

class filebak(object):
	def __init__(self, file, ext):
		self.file = file
		self.ext = ext

	def fbak(self):
		if os.path.isfile(self.file+self.ext):
			print (self.file + self.ext + " already exists")
		else:
			print ("backing up", repr(self.file), "as", self.file + self.ext)
			proc = subprocess.Popen(['cp', self.file, self.file + self.ext], stderr=subprocess.PIPE)
			proc.communicate()[0]

class filereplace(object):
	def __init__(self, file, find, replace):
		self.file = file
		self.find = find
		self.replace = replace
		
	def freplace(self):
		with open(self.file, 'a+') as f:
			print ("finding: ", repr(self.find), self.file)
			print ("replacing with: ", repr(self.replace), self.file)
			for line in fileinput.input(self.file, inplace=1):
				line = line.replace(self.find, self.replace)
				sys.stdout.write(line)
			f.close
		with open(self.file, 'r') as f:
			f.seek(0)
			sys.stdout.write(f.read())
			f.close

class filecp(object):
	def __init__(self, src, dst):
		self.src = src
		self.dst = dst
	
	def fcp(self):
		shutil.copy2(self.src, self.dst)
		print ("Copying " + self.src + " to " + self.dst)
		#folder = os.path.dirname(os.path.abspath(dst))
		print (glob.glob(self.dst))
		
		
		
#TEST
#file = "/etc/sysctl.conf"
#append = "\nnet.ipv4.ip_forward=1"
#ip_forward = fmanip(file, append)
#filebak(file, ".bak").fbak()
#fileappend(file, append).fappend()

#file = "/etc/systemd/system/vncserver@:4.service"
#filebak(file, ".bak").fbak()
#find = "<USER>"
#replace = "ur.local"
#filereplace(file, find, replace).freplace()

#file = "/etc/systemd/system/vncserver@:4.service"
#find = "\"/usr/bin/vncserver %i\""
#replace = "\"/usr/bin/vncserver %i -geometry 1280x1024\""
#filereplace(file, find, replace).freplace()

#src = '/lib/systemd/system/vncserver@.service'
#dst = '/etc/systemd/system/vncserver@:4.service'
#filecp(src, dst).fcp()