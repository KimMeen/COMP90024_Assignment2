import openstack as OS
import sys
import openStackConnect as OSConnect
import openStackInfo as OSInfo

# Initialize cloud
conn = OS.connect(cloud='openstack')
OSInfo.list_ips(conn)