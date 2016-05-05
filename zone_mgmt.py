#! python
import os
import subprocess
import re

class nmcli_con_enum(object):
	def __init__(self):
		self.device_list = []
		self.ext_dev = []
		
	def dev_enum(self):
		#identify all attached and recognizable NICs
		nmcli_show = subprocess.Popen(('nmcli', '-f', 'GENERAL.DEVICE','device', 'show'), stdout=subprocess.PIPE)
		device_string = re.sub('^(.*?\s+)', "", (nmcli_show.stdout.read()).decode("ascii"), flags=re.MULTILINE)
		#build a list of sublists, listing (device_id,ip)
		for i in device_string.splitlines():
			nmcli_ip = subprocess.Popen(('nmcli', '-f', 'IP4.ADDRESS','device', 'show', i), stdout=subprocess.PIPE)
			ip_string = re.sub('^(.*?\s+)', "", (nmcli_ip.stdout.read()).decode("ascii"), flags=re.MULTILINE)
			for j in ip_string.splitlines():
				#print(i,j)
				dev_i = (i,j)
				#print(dev_i)
				self.device_list.append(dev_i)
		print(self.device_list)

	#if 192.168.0.1 is assigned to a NIC, set it to internal
	#for all others, enumerate an iteration table, for each iterable attempt to ping google
	#if ping successful, assign nic to external, assign all others to internal
	def dev_zone(self):
		for x in [dev for (dev,ip) in self.device_list if ip=="192.168.0.1/24"]:
			print('Found internal ip on:',x)
			subprocess.Popen(['nmcli', 'con', 'mod', x, 'connection.zone', 'internal'])
		else:
			ping_dev = ([dev for (dev,ip) in self.device_list if ip !="192.168.0.1/24" if dev!="lo"])
			for x in ping_dev:
				print('Testing:',x)
				try:
					subprocess.check_output(('ping', '-c', '3', '-I', x, 'google.com'), \
					stderr=subprocess.STDOUT)
					print('Success:',x)
					self.ext_dev.append(x)
					subprocess.Popen(['nmcli', 'con', 'mod', x, 'connection.zone', 'external'])
				except Exception:
					print('Error:',x)
					subprocess.Popen(['nmcli', 'con', 'mod', x, 'connection.zone', 'internal'])
					continue
		print(self.ext_dev)

	def dev_nat(self):
		try:
			#Configure masquerading on the externally facing device:
			print("Configuring masquerade on external zone")
			subprocess.Popen(['firewall-cmd', '--permanent', '--zone=external', '--add-masquerade'])
			#Configure NAT rule for internal traffic to freely passthrough to external network
			for x in self.ext_dev:
				print("Configuring NAT rule for internal traffic to passthru to external network:", x)
				fw = subprocess.Popen(['firewall-cmd', '--permanent', '--direct', '--passthrough', \
				'ipv4', '-t', 'nat', '-I', 'POSTROUTING', '-o', x, '-j' 'MASQUERADE', '-s', '192.168.0.0/24'],\
				stderr=subprocess.PIPE)
				fw.communicate()[0]
				fw.wait
		except Exception as e:
			print(x)
			print(e)
			
	def main(self):
		self.dev_enum()
		self.dev_zone()
		self.dev_nat()


#TEST! -place in main
#instantiate nmcli_con_enum() and run main()
#nmcli_con_enum().main()