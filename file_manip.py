#! python
import os
import subprocess
import re
import fileinput


#define a method of backing up a file, then append a string to the file and finally read the file
def file_manip(file, append):
	class file_org:
		if os.path.isfile(file+"org"):
			print (file + ".org already exists")
		else:
			print ("backing up", repr(file), "as", file + ".org")
			proc = subprocess.Popen(['mv', file, file + ".org"], stderr=subprocess.PIPE)
			proc.communicate()[0]
			proc.kill()
	
	class file_a:
		f = open(file, 'a+')
		#print(f)
		print ("appending", repr(append), file)
		f.write(append)
		f.seek(0)
		print(f.read())
		f.close

		
		
class fmanip(object):
	def __init__(self,file,append):
		self.file = file
		self.append = append
		
	def fbak(self):
		if os.path.isfile(self.file+"bak"):
			print (self.file + ".bak already exists")
		else:
			print ("backing up", repr(self.file), "as", self.file + ".bak")
			proc = subprocess.Popen(['mv', self.file, self.file + ".bak"], stderr=subprocess.PIPE)
			proc.communicate()[0]
			proc.kill()
	
	def fappend(self):
		f = open(self.file, 'a+')
		#print(f)
		print ("appending", repr(self.append), file)
		f.write(self.append)
		f.seek(0)
		print(f.read())
		f.close
		
		
		
#TEST
#call the file manip method for ip_forwarding
#file = "/etc/sysctl.conf"
#append = "\nnet.ipv4.ip_forward=1"
#file_manip(file, append)