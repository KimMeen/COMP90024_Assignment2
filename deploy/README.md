# Environment and Configuration

This repo includes configuration scripts. 
Deployment is achieved with the help of provisioning tools(openstackSDK(python)).
Ansible will be used to automate the process as well.


## Databases(CouchDB)
Public address is mapped using ngrok's mapping service. (This is only used for remote testing)
For Example: http://xxxxxxx.ngrok.io's port 80 is mapped to port 5984 of the nectar instance, which is then mapped to the container's port 5984.

After harvester can be implemented, It will scrawl the data directly to local database(couchdb).

The couchDB Cluster will deal with data synchronization by itself.
(If one database is create on single node. At the same time, It will be accessiable in all other nodes).

To Prevent data lose. Replication will be implemented.


Master Node: 
Public: http://b8951816.ngrok.io
Private(Access Through Student VPN): 172.26.37.209

Slave Node 1:
Public: http://0782f7b0.ngrok.io
Private(Access Through Student VPN): 172.26.37.193

Slave Node 2:
Public: http://3722a596.ngrok.io
Private(Access Through Student VPN): 172.26.37.196

Slave Node 3:
Public: http://782e8f7f.ngrok.io
Private(Access Through Student VPN): 172.26.37.207

> User Name: admin
> User Password: admin