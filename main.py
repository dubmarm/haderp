#! python
import os
import subprocess
import re
import fileinput

#Call fmanip to append ipforwarding
ip_forward = fmanip("/etc/sysctl.conf","\nnet.ipv4.ip_forward=1")
ip_forward.fbak()
ip_forward.fappend()

#Call method for enabling ipforwarding
class ip_forward_cmd:
 subprocess.Popen(['sysctl', '-w', 'net.ipv4.ip_forward=1'])
 
#centos has only 1 route, so with two nics you will run into issues
#hard define the preferred route device.
#call the file_manip method for /etc/sysconfig/network
#append gateway
gate_dev = ",".join(nmcli_con_enum.ext_dev)
append = "\nGATEWAYDEV=" + gate_dev
gateway = fmanip("/etc/sysconfig/network",append)
gateway.fbak()
ip_forward.fappend()