#! python
import os
import subprocess
import re
import fileinput
import zone_mgmt.py
import file_manip.py

#Call fmanip to append ipforwarding
ip_forward = fmanip("/etc/sysctl.conf","\nnet.ipv4.ip_forward=1")
ip_forward.fbak()
ip_forward.fappend()

#Call method for enabling ipforwarding
class ip_forward_cmd:
 subprocess.Popen(['sysctl', '-w', 'net.ipv4.ip_forward=1'])
 
#configure firewall zones
devices = nmcli_con_enum()
devices.dev_enum()
devices.dev_zone()

#hard define the preferred route device.
#append gateway
gateway = nmcli_con_enum()
gateway.dev_enum()
gateway.dev_zone.ext_dev()
gate_dev = ",".join(nmcli_con_enum.ext_dev)
append = "\nGATEWAYDEV=" + gate_dev
gateway = fmanip("/etc/sysconfig/network",append)
gateway.fbak()
ip_forward.fappend()