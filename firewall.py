#!python
import os
import subprocess

#Configure Firewall Ports/Services Class
class firewall_port(object):
	def __init__(self, zone, port, proto):
		self.zone = zone
		self.port = port
		self.proto = proto
	
	def fw_port(self):
		try:
			print("Adding to firewall:", self.zone, ":", self.port, ":", self.proto)
			fw = subprocess.Popen(['firewall-cmd', '--permanent', '--zone=' + self.zone, \
			'--add-port=' + self.port + '/' + self.proto], stderr=subprocess.PIPE)
			fw.communicate()[0]
			fw.wait()
		except Exception as e:
			print(self.port)
			print(e)
	#firewall.fw_port("internal", "8140", "tcp")

class firewall_service(object):
	def __init__(self, zone, service):
		self.zone = zone
		self.service = service
	
	def fw_service(self):
		try:
			print("Adding to firewall:", self.zone, ":", self.service)
			fw = subprocess.Popen(['firewall-cmd', '--permanent', '--zone=' + self.zone, \
			'--add-service=' + self.service])
			fw.communicate()[0]
			fw.wait()
		except Exception as e:
			print(self.service)
			print(e)
	#firewall.fw_service("internal", "ssh")
	
def fw_reload():
	try:
		print("Reloading Firewall")
		fw = subprocess.Popen(['firewall-cmd', '--complete-reload'])
		fw.wait
		fw = subprocess.Popen(['firewall-cmd', '--list-all-zones'])
		fw.wait()
	except Exception as e:
		print(e)


#TEST! -place in main	
#port8140 = firewall_port("internal", "8140", "tcp")
#port8140.fw_port()
#fssh = firewall_service("internal", "ssh")
#fssh.fw_service()
#fw_reload()
