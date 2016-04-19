#http://www.frankmcsherry.org/graph/scalability/cost/2015/01/15/COST.html
#http://www.frankmcsherry.org/graph/scalability/cost/2015/02/04/COST2.html
#http://www.michael-noll.com/tutorials/running-hadoop-on-ubuntu-linux-multi-node-cluster/
#http://bradhedlund.com/2011/09/10/understanding-hadoop-clusters-and-the-network/
#https://en.wikipedia.org/wiki/Fallacies_of_distributed_computing
#https://news.ycombinator.com/item?id=9581862

#http://www.cs.put.poznan.pl/csobaniec/software/python/py-qrc.html

#install basic SERVER WITH GUI

import os
import subprocess
import re

#define a method of backing up a file, then append a string to the file and finally reading the file
def file_manip(file, append):
	class file_org:
		if os.path.isfile(file+"org"):
			print (file + ".org already exists")
		else:
			print ("backing up", repr(file), "as", file + ".org")
			proc = subprocess.Popen(['mv', file, file + ".org"], stderr=subprocess.PIPE)
			proc.communicate()[0]
	
	class file_a:
		f = open(file, 'a+')
		#print(f)
		print ("appending", repr(append), file)
		f.write(append)
		f.seek(0)
		print(f.read())
		f.close
	
#call the file manip method for ip_forwarding
file = "/etc/sysctl.conf"
append = "\nnet.ipv4.ip_forward=1"
file_manip(file, append)
	
class ip_forward_cmd:
	subprocess.Popen(['sysctl', '-w', 'net.ipv4.ip_forward=1'])


#configure zone management
#assigning interfaces to zones MUST be performed by nmcli
#https://access.redhat.com/discussions/1455033

# nmcli pipe grep all devices on computer into list, along with their IP address
#http://stackoverflow.com/questions/7876272/select-value-from-list-of-tuples-where-condition
class nmcli_con_enum:
	#identify all attached and recognizable NICs
	nmcli_show = subprocess.Popen(('nmcli', '-f', 'GENERAL.DEVICE','device', 'show'), stdout=subprocess.PIPE)
	device_string = re.sub('^(.*?\s+)', "", (nmcli_show.stdout.read()).decode("ascii"), flags=re.MULTILINE)
	#build a list of sublists, listing (device_id,ip)
	device_list = []
	for i in device_string.splitlines():
		nmcli_ip = subprocess.Popen(('nmcli', '-f', 'IP4.ADDRESS','device', 'show', i), stdout=subprocess.PIPE)
		ip_string = re.sub('^(.*?\s+)', "", (nmcli_ip.stdout.read()).decode("ascii"), flags=re.MULTILINE)
		for j in ip_string.splitlines():
			#print(i,j)
			dev_i = (i,j)
			#print(dev_i)
			device_list.append(dev_i)
	print(device_list)
	#if 192.168.0.1 is assigned to a NIC, set it to internal
	#for all others, enumerate an iteration table, for each iterable attempt to ping google
	#if ping successful, assign nic to external, assign all others to internal
	
	for x in [dev for (dev,ip) in device_list if ip=="192.168.0.1/24"]:
		print('Found internal ip on:',x)
		subprocess.Popen(['nmcli', 'con', 'mod', x, 'connection.zone', 'internal'])
	else:
		ping_dev = ([dev for (dev,ip) in device_list if ip !="192.168.0.1/24" if dev!="lo"])
		ext_dev = []
		for x in ping_dev:
			print('Testing:',x)
			try:
				subprocess.check_output(('ping', '-c', '3', '-I', x, 'google.com'), stderr=subprocess.STDOUT)
				print('Success:',x)
				ext_dev.append(x)
				subprocess.Popen(['nmcli', 'con', 'mod', x, 'connection.zone', 'external'])
			except Exception:
				print('Error:',x)
				subprocess.Popen(['nmcli', 'con', 'mod', x, 'connection.zone', 'internal'])
				continue
	print(ext_dev)

#centos has only 1 route, so with two nics you will run into issues
#hard define the preferred route device.
#call the file_manip method for /etc/sysconfig/network
#append gateway
file = "/etc/sysconfig/network"
gate_dev = ",".join(nmcli_con_enum.ext_dev)
append = "\nGATEWAYDEV=" + gate_dev
file_manip(file, append)

class firewall:
	def fw_port(zone, port, proto):
		try:
			fw = subprocess.Popen(['firewall-cmd', '--permanent', '--zone=' + zone, '--add-port=' + port + '/' + proto], stderr=subprocess.PIPE)
			fw.communicate()[0]
			fw.wait
		except Exception as e:
			print(port)
			print(e)
#firewall.fw_port("internal", "8140", "tcp")
		
	def fw_service(zone, service):
		try:
			fw = subprocess.Popen(['firewall-cmd', '--permanent', '--zone=' + zone, '--add-service=' + service])
			fw.communicate()[0]
			fw.wait
		except Exception as e:
			print("Error")
			print(e)
#firewall.fw_service("internal", "ssh")

port_list = [
	50070, # allow NameNodeWebUI
	50470, # allow NameNodeWebUI
	8020, # allow NameNodeMetaData
	9000, # allow NameNodeMetaData
	50075, # allow DataNode
	50475, # allow DataNode
	50010, # allow DataNode
	50020, # allow DataNode
	50090, # allow SecondaryNameNode
	];
print(port_list)
for x in port_list:
	firewall.fw_port("internal", str(x), "tcp")		
