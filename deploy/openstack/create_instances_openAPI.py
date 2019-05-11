import openstack as OS
import sys
import openStackConnect as OSConnect
import openStackInfo as OSInfo

# # Initialize and turn on debug logging
# openstack.enable_logging(
#     debug=True, path='openstack.log', stream=sys.stdout)

# Initialize cloud
conn = OS.connect(cloud='openstack')
OSConnect.create_server(conn, sys.argv[1])


    