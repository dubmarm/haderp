#! python
import os
import subprocess
import re
import fileinput


#define a class of backing up a file, then append a string to the file and finally read the file
class fmanip(object):
	def __init__(self, file, append):
		self.file = file
		self.append = append
		
	def fbak(self):
		if os.path.isfile(self.file+"bak"):
			print (self.file + ".bak already exists")
		else:
			print ("backing up", repr(self.file), "as", self.file + ".bak")
			proc = subprocess.Popen(['mv', self.file, self.file + ".bak"], stderr=subprocess.PIPE)
			proc.communicate()[0]
	
	def fappend(self):
		f = open(self.file, 'a+')
		#print(f)
		print ("appending", repr(self.append), file)
		f.write(self.append)
		f.seek(0)
		print(f.read())
		f.close
		
#TEST
#ip_forward = fmanip("/etc/sysctl.conf","\nnet.ipv4.ip_forward=1")
#ip_forward.fbak()
#ip_forward.fappend()
