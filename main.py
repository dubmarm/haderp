#! python
import os
import subprocess
import re
import fileinput
import zone_mgmt
import file_manip
import firewall

#Call fmanip to append ipforwarding
ipforward_file = "/etc/sysctl.conf"
ipforward_append = "\nnet.ipv4.ip_forward=1"
file_manip.filebak(ipforward_file, ".bak").fbak()
file_manip.fileappend(ipforward_file, ipforward_append).fappend()


#Call method for enabling ipforwarding
class ip_forward_cmd:
 subprocess.Popen(['sysctl', '-w', 'net.ipv4.ip_forward=1'])
 
#configure firewall zones
zone_mgmt.nmcli_con_enum().main()

#hard define the preferred route device.
#append gateway
gateway = zone_mgmt.nmcli_con_enum()
gateway.dev_enum()
gateway.dev_zone()
gateway_device = ",".join(gateway.ext_dev)

gateway_file = "/etc/sysconfig/network"
gateway_append = "\nGATEWAYDEV=" + gateway_device
file_manip.filebak(gateway_file, ".bak").fbak()
file_manip.fileappend(gateway_file, gateway_append).fappend()

#configure firewall
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
	print(x[0], x[1])
	firewall.firewall_service(x[0], x[1]).fw_service()

#GENERAL PORTS
port_list = [
	#HDFS PORTS
	("internal", 8020, "tcp"), # allow NameNodeMetaData : dfs.namenode.rpc-address
	("internal", 8010, "tcp"), # allow DataNode : dfs.datanode.ipc.address
	("internal", 8480, "tcp"), # allow DataNode : dfs.journalnode.http-address
	("internal", 8481, "tcp"), # allow DataNode : dfs.journalnode.https-address
	("internal", 8485, "tcp"), # allow DataNode : dfs.journalnode.rpc-address
	("internal", 9000, "tcp"), # allow NameNodeMetaData
	("internal", 50070, "tcp"), # allow NameNodeWebUI : namenode.http-address
	("internal", 50075, "tcp"), # allow DataNode : dfs.datanode.http.address
	("internal", 50475, "tcp"), # allow DataNode : dfs.datanode.https.address
	("internal", 50470, "tcp"), # allow NameNodeWebUI : dfs.https.port
	("internal", 50010, "tcp"), # allow DataNode : dfs.datanode.address
	("internal", 50020, "tcp"), # allow DataNode :
	("internal", 50100, "tcp"), # allow DataNode : dfs.namenode.backup.address
	("internal", 50090, "tcp"), # allow SecondaryNameNode : dfs.namenode.secondary.http-address
	("internal", 50105, "tcp"), # allow NameNode : dfs.namenode.backup.http-address
	("internal", 50091, "tcp"), # allow SecondaryNameNode : dfs.namenode.secondary.https-address
	#PUPPET PORTS
	("internal", 8140,"tcp"), # allow puppetmaster
	#AMBARI PORTS
	####8080 is a conflict port!!!!
	("internal", 8080, "tcp"), # allow Ambari Server : confirmed
	("internal", "8440-8443", "tcp"), # allow Ambari Server : confirmed
	("internal", 61310, "tcp"), # allow Ambari Metrics : hbase.master.info.port
	("internal", 61300, "tcp"), # allow Ambari Metrics : hbase.master.port
	("internal", 61330, "tcp"), # allow Ambari Metrics : hbase.regionserver.info.port
	("internal", 61320, "tcp"), # allow Ambari Metrics : hbase.regionserver.port
	("internal", 61388, "tcp"), # allow Ambari Metrics : hbase.zookeeper.leaderport
	("internal", 61288, "tcp"), # allow Ambari Metrics : hbase.zookeeper.peerport
	#KAFKA PORTS
	("internal", 6667, "tcp"), # allow Kafka Broker : confirmed
	("internal", 8671, "tcp"), # allow Kafka Metrics : confirmed
	#YARN PORTS
	("internal", 8025, "tcp"), # allow YARNResourceManager
	("internal", 8141, "tcp"), # allow YARNRMAdmin
	("internal", 8050, "tcp"), # allow YARNContainerManager
	("internal", 45454, "tcp"), # allow YARNApplicationsManager
	("internal", 8042, "tcp"), # allow YARNNodeManagerWebApp
	("internal", 8088, "tcp"), # allow YARNResourceManagerWebApp
	#YARN PORTS
	("internal", 2181, "tcp"), # allow YARNResourceManager : yarn.resourcemanager.zk-address
	("internal", 8025, "tcp"), # allow YARNResourceManager : yarn.resourcemanager.resource-tracker.address
	("internal", 8141, "tcp"), # allow YARNRMAdmin : yarn.resourcemanager.admin.address
	("internal", 8030, "tcp"), # allow YARNResourceManager : yarn.resourcemanager.scheduler.address
	("internal", 10200, "tcp"), # allow YARNTimeline : yarn.timeline-service.address
	("internal", 8050, "tcp"), # allow YARNContainerManager : yarn.resourcemanager.address
	("internal", 45454, "tcp"), # allow YARNApplicationsManager : yarn.nodemanager.address
	("internal", 8042, "tcp"), # allow YARNNodeManagerWebApp : yarn.nodemanager.webapp.address
	("internal", 8088, "tcp"), # allow YARNResourceManagerWebApp : yarn.resourcemanager.webapp.address
	("internal", 8188, "tcp"), # allow YARN : yarn.timeline-service.webapp.address
	("internal", 8047, "tcp"), # allow YARN :yarn.sharedcache.admin.address
	("internal", 8045, "tcp"), # allow YARN :yarn.sharedcache.client-server.address
	("internal", 8190, "tcp"), # allow YARNTimeline :yarn.timeline-service.webapp.https.address
	("internal", 8040, "tcp"), # allow YARNNodeManager : yarn.nodemanager.localizer.address
	("internal", 8090, "tcp"), # allow YARNResourceManager : yarn.resourcemanager.webapp.https.address
	("internal", 8046, "tcp"), # allow YARNSharedCache : yarn.sharedcache.uploader.server.address
	("internal", 8788, "tcp"), # allow YARNSharedCache : yarn.sharedcache.webapp.address
	#MAPREDUCE PORTS
	("internal", 50030,"tcp"), # allow JobTrackerWebUI
	("internal", 8021,"tcp"), # allow JobTracker
	("internal", 50060,"tcp"), # allow TaskTrackerWebUI
	("internal", 51111,"tcp"), # allow HistoryServerWebUI
	("internal", 19888,"tcp"), # allow HistoryServerWebUI
	#MAPREDUCE PORTS
	("internal", 50030, "tcp"), # allow JobTrackerWebUI : mapreduce.jobtracker.http.address
	("internal", 8021, "tcp"), # allow JobTracker : confirmed
	("internal", 10033, "tcp"), # allow JobTracker : mapreduce.jobhistory.admin.address
	("internal", 50060, "tcp"), # allow TaskTrackerWebUI/Shuffle : mapreduce.tasktracker.http.address
	("internal", 51111, "tcp"), # allow HistoryServerWebUI
	("internal", 19888, "tcp"), # allow HistoryServerWebUI : yarn.log.server.url / mapreduce.jobhistory.webapp.address
	("internal", 13562, "tcp"), # allow MapRShuffle : mapreduce.shuffle.port
	("internal", 10020, "tcp"), # allow JobHistory : mapreduce.jobhistory.address
	#HBASE PORTS
	("internal", 60000, "tcp"), # allow HMaster
	("internal", 60010, "tcp"), # allow HMasterWebUI
	("internal", 60020, "tcp"), # allow RegionServer
	("internal", 60030, "tcp"), # allow RegionServer
	("internal", 2888, "tcp"), # allow RegionServer : hbase.zookeeper.peerport
	("internal", 3888, "tcp"), # allow RegionServer : hbase.zookeeper.leaderport
	("internal", 2181, "tcp"), # allow RegionServer : hbase.zookeeper.property.clientPort
	("internal", 16000, "tcp"), # allow HBase Server : hbase.master.port
	("internal", 16010, "tcp"), # allow HBase Server : hbase.master.info.port
	("internal", 16020, "tcp"), # allow HBase Server : hbase.regionserver.port
	("internal", 16030, "tcp"), # allow HBase Server : hbase.regionserver.info.port
	("internal", 16100, "tcp"), # allow HBase Server : hbase.status.multicast.address.port
	#CONFLICT WITH AMBARI PORT!!!!!!
	("internal", 8080, "tcp"), # allow HBase Server : hbase.rest.port
	#TITAN PORT
	("internal", 8182, "tcp"), # allow Titan
	#GANGLIA PORTS
	("internal", "8660-8663","tcp"), # allow GangliaServer
	("internal", 8651,"tcp"), # allow GangliaServer
	#POSTGRES PORT
	("internal", 5432,"tcp"), # allow PostGres
	#TIGERVNC
	("internal",5904,"tcp"), # allow TigerVNC
	("external",5904,"tcp"), # allow TigerVNC
	];
print(port_list)
for x in port_list:
	firewall.firewall_port(x[0], str(x[1]), x[2]).fw_port()

firewall.fw_reload()



#CONFIGURE VNCSERVER
# yum install -y tigervnc-server
# sudo cp /lib/systemd/system/vncserver@.service /etc/systemd/system/vncserver@:4.service

file = "/etc/systemd/system/vncserver@:4.service"
filebak(file, ".bak").fbak()
find = "<USER>"
replace = "ur.local"
filereplace(file, find, replace).freplace()

file = "/etc/systemd/system/vncserver@:4.service"
find = "\"/usr/bin/vncserver %i\""
replace = "\"/usr/bin/vncserver %i -geometry 1280x1024\""
filereplace(file, find, replace).freplace()

# systemctl daemon-reload
# systemctl enable vncserver@:4.service
# ssh ur.local@192.168.0.1
# vncserver
	# password
# exit
# rm -i /tmp/.X11-unix/X4
# sudo systemctl daemon-reload
# sudo systemctl restart vncserver@:4.service
#	download VNCViewer for Windows
#	192.168.0.1:5904





