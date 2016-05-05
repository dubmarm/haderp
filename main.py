#! python
import os
import subprocess
import re
import fileinput
import zone_mgmt
import file_manip
import firewall

#Call fmanip to append ipforwarding
#ip_forward = file_manip.fmanip("/etc/sysctl.conf","\nnet.ipv4.ip_forward=1")
#ip_forward.fbak()
#ip_forward.fappend()

#Call method for enabling ipforwarding
#class ip_forward_cmd:
# subprocess.Popen(['sysctl', '-w', 'net.ipv4.ip_forward=1'])
 
#configure firewall zones
#zone_mgmt.nmcli_con_enum().main()

#hard define the preferred route device.
#append gateway
gateway = zone_mgmt.nmcli_con_enum()
gateway.dev_enum()
gateway.dev_zone()
gateway_device = ",".join(gateway.ext_dev)
gateway_append = "\nGATEWAYDEV=" + gateway_device
print gateway_append
gateway = file_manip.fmanip("/etc/sysconfig/network", gateway_append)
gateway.fbak()
gateway.fappend()
