import cinderclient
import openstack as OS
import sys
import openStackConnect as OSConnect
import openStackInfo as OSInfo
from keystoneauth1 import loading
from keystoneauth1 import session
from cinderclient import client
from openStackConfig import *
import sys
conn = OS.connect(cloud="openstack_group")
server = conn.compute.find_server(sys.argv[1])
# print (server.id)
loader = loading.get_plugin_loader('password')
auth = loader.load_from_options(auth_url="https://keystone.rc.nectar.org.au:5000/v3/",username="m.gao8@student.unimelb.edu.au", password="YWMxMDc4MTU3MDY1MDhj",project_id="a2f5f4d6a2724e09bd9c0ff81e2ece12",user_domain_name="Default")
sess = session.Session(auth=auth)
cinder = client.Client("3",session=sess)
cinder.volumes.list()
volumn = cinder.volumes.get(VOLUMES_MAP[sys.argv[2]])
print ("nova volume-attach " + server.id + " " + VOLUMES_MAP[sys.argv[2]])
# cinder.volumes.attach(volumn, server.id, "/dev/vdc", host_name=sys.argv[1])
# cinder.volumes.detach(volumn)

# cinder attachment-show --os-user-id OS_USER_ID --os-username OS_USERNAME --os-user-domain-id OS_USER_DOMAIN_ID --os-user-domain-name OS_USER_DOMAIN_NAME --os-password OS_PASSWORD