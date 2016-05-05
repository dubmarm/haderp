#!python
import os
import subprocess

#Configure Firewall Ports/Services Class
class firewall(object):
	def __init__(self):
		self.firewall = []
	
	def fw_port(self, zone, port, proto):
		try:
			print("Adding to firewall:", zone, ":", port, ":", proto)
			fw = subprocess.Popen(['firewall-cmd', '--permanent', '--zone=' + zone, \
			'--add-port=' + port + '/' + proto], stderr=subprocess.PIPE)
			fw.communicate()[0]
			fw.wait
		except Exception as e:
			print(port)
			print(e)
	#firewall.fw_port("internal", "8140", "tcp")

	def fw_service(self, zone, service):
		try:
			print("Adding to firewall:", zone, ":", service)
			fw = subprocess.Popen(['firewall-cmd', '--permanent', '--zone=' + zone, \
			'--add-service=' + service])
			fw.communicate()[0]
			fw.wait
		except Exception as e:
			print("Error")
			print(e)
	#firewall.fw_service("internal", "ssh")
	
	def fw_passthru(self):
		#print(nmcli_con_enum.ext_dev)
		try:
			#Configure masquerading on the externally facing device:
			print("Configuring masquerade on external zone")
			subprocess.Popen(['firewall-cmd', '--permanent', '--zone=external', '--add-masquerade'])
			#Configure NAT rule for internal traffic to freely passthrough to external network
			for x in nmcli_con_enum.ext_dev:
				print("Configuring NAT rule for internal traffic to passthru to external network:", x)
				fw = subprocess.Popen(['firewall-cmd', '--permanent', '--direct', '--passthrough', \
				'ipv4', '-t', 'nat', '-I', 'POSTROUTING', '-o', x, '-j' 'MASQUERADE', '-s', '192.168.0.0/24'],\
				stderr=subprocess.PIPE)
				fw.communicate()[0]
				fw.wait
		except Exception as e:
			print(x)
			print(e)
	
	def fw_reload(self):
		try:
			print("Reloading Firewall")
			fw = subprocess.Popen(['firewall-cmd', '--complete-reload'])
			fw.wait
			fw = subprocess.Popen(['firewall-cmd', '--list-all-zones'])
			fw.wait
		except Exception as e:
			print(e)