import openstack as OS
import sys
import openStackConnect as OSConnect
import openStackInfo as OSInfo

# Initialize cloud
conn = OS.connect(cloud=sys.argv[1])
server = OSConnect.create_server(conn, sys.argv[2])

# import openstack as OS
# import sys
# import openStackConnect as OSConnect
# import openStackInfo as OSInfo
# conn = OS.connect(cloud="openstack_group")