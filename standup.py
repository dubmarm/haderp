#install basic SERVER WITH GUI
#Programmed for Python 3.5
#https://github.com/dubmarm/haderp.git

import os
import subprocess
import re

#define a method of backing up a file, then append a string to the file and finally read the file
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
				subprocess.check_output(('ping', '-c', '3', '-I', x, 'google.com'), \
				stderr=subprocess.STDOUT)
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


#Configure Firewall Ports/Services
	#https://lists.fedorahosted.org/pipermail/firewalld-users/2013-February/000049.html
	#https://bluehatrecord.wordpress.com/2014/04/17/logging-packet-drops-in-firewalld/
	#http://www.thegeekstuff.com/2012/08/iptables-log-packets/
	#http://www.tecmint.com/configure-firewalld-in-centos-7/2/
class firewall:
	def fw_port(zone, port, proto):
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
		
	def fw_service(zone, service):
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
	
	def fw_passthru():
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
	
	def fw_reload():
		try:
			print("Reloading Firewall")
			fw = subprocess.Popen(['firewall-cmd', '--complete-reload'])
			fw.wait
			fw = subprocess.Popen(['firewall-cmd', '--list-all-zones'])
			fw.wait
		except Exception as e:
			print(e)
			
firewall.fw_passthru()
	
#GENERAL SERVICES
service_list = [
	("internal", "tftp"),
	("internal", "ftp"),
	("internal", "dns"),
	("internal", "nfs"),
	("internal", "http"),
	("external", "http"),
	("internal", "https"),
	("external", "https"),
	("internal", "ssh"),
	("external", "ssh"),
	("internal", "proxy-dhcp"),
	("internal", "ntp"),
	]
print(service_list)
for x in service_list:
	firewall.fw_service(x[0], x[1])	

#GENERAL PORTS
port_list = [
	#HDFS PORTS
	("internal", 50070, "tcp"), # allow NameNodeWebUI
	("internal", 50470, "tcp"), # allow NameNodeWebUI
	("internal", 8020, "tcp"), # allow NameNodeMetaData
	("internal", 9000, "tcp"), # allow NameNodeMetaData
	("internal", 50075, "tcp"), # allow DataNode
	("internal", 50475, "tcp"), # allow DataNode
	("internal", 50010, "tcp"), # allow DataNode
	("internal", 50020, "tcp"), # allow DataNode
	("internal", 50090, "tcp"), # allow SecondaryNameNode
	#PUPPET PORTS
	("internal",8140,"tcp"), # allow puppetmaster
	("internal",61613,"tcp"), # allow puppet mcollective
	("internal",8142,"tcp"), # allow puppet orchestration
	#AMBARI PORTS
	("internal",8080,"tcp"), # allow Ambari Server
	("internal","8440-8443","tcp"), # allow Ambari Server
	#YARN PORTS
	("internal",8025,"tcp"), # allow YARNResourceManager
	("internal",8141,"tcp"), # allow YARNRMAdmin
	("internal",8050,"tcp"), # allow YARNContainerManager
	("internal",45454,"tcp"), # allow YARNApplicationsManager
	("internal",8042,"tcp"), # allow YARNNodeManagerWebApp
	("internal",8088,"tcp"), # allow YARNResourceManagerWebApp	
	#MAPREDUCE PORTS
	("internal",50030,"tcp"), # allow JobTrackerWebUI
	("internal",8021,"tcp"), # allow JobTracker
	("internal",50060,"tcp"), # allow TaskTrackerWebUI
	("internal",51111,"tcp"), # allow HistoryServerWebUI
	("internal",19888,"tcp"), # allow HistoryServerWebUI	
	#HIVE PORTS
	("internal",10000,"tcp"), # allow HiveServer2
	("internal",9083,"tcp"), # allow HiveMetaStore
	#HBASE PORTS
	("internal",60000,"tcp"), # allow HMaster
	("internal",60010,"tcp"), # allow HMasterWebUI
	("internal",60020,"tcp"), # allow RegionServer
	("internal",60030,"tcp"), # allow RegionServer
	("internal",2888,"tcp"), # allow RegionServer
	("internal",3888,"tcp"), # allow RegionServer
	("internal",2181,"tcp"), # allow RegionServer
	#WEBHCAT PORTS
	("internal",50111,"tcp"), # allow WebHCatServer
	#GANGLIA PORTS
	("internal","8660-8663","tcp"), # allow GangliaServer
	("internal",8651,"tcp"), # allow GangliaServer
	#MYSQL PORTS
	("internal",3306,"tcp"), # allow MySQL
	#TIGERVNC
	("internal","5904-5905","tcp"), # allow TigerVNC
	];
print(port_list)
for x in port_list:
	firewall.fw_port(x[0], str(x[1]), x[2])

firewall.fw_reload()
exit()
