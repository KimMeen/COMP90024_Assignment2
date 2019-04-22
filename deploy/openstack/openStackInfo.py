from openStackConfig import NETWORK_NAME
def list_servers(conn):
    print("List Servers:")

    for server in conn.compute.servers():
        print(server)
        print(server.addresses[NETWORK_NAME][0]['addr'])

def list_ips(conn):
    print("List Server IPs:")
    for server in conn.compute.servers():
        print(server.name + ": " + server.addresses[NETWORK_NAME][0]['addr'])

def list_images(conn):
    print("List Images:")

    for image in conn.compute.images():
        print(image)

def list_flavors(conn):
    print("List Flavors:")

    for flavor in conn.compute.flavors():
        print(flavor)

def list_networks(conn):
    print("List Networks:")

    for network in conn.network.networks():
        print(network)

def list_security_groups(conn):
    print("List Security Groups:")

    for port in conn.network.security_groups():
        print(port)