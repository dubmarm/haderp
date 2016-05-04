#! python

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

	
	
class nmcli_con
