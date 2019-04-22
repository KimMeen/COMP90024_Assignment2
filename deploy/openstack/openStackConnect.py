import os
import errno
from openStackConfig import *

def create_keypair(conn):
    keypair = conn.compute.find_keypair(KEYPAIR_NAME)

    if not keypair:
        print("Create Key Pair:")

        keypair = conn.compute.create_keypair(name=KEYPAIR_NAME)

        print(keypair)

        try:
            os.mkdir(SSH_DIR)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e

        with open(PRIVATE_KEYPAIR_FILE, 'w') as f:
            f.write("%s" % keypair.private_key)

        os.chmod(PRIVATE_KEYPAIR_FILE, 0o400)

    return keypair



def create_server(conn, server_name):
    print("Create Server:")

    image = conn.compute.find_image(IMAGE_NAME)
    flavor = conn.compute.find_flavor(FLAVOR_NAME)
    network = conn.network.find_network(NETWORK_NAME)
    security_groups = []
    for group_name in SECURITY_GROUPS:
        group = {}
        group_detail = conn.network.find_security_group(group_name)
        group['name'] = group_detail.name
        security_groups.append(group)
    keypair = create_keypair(conn)

    server = conn.compute.create_server(
        name=server_name, image_id=image.id, flavor_id=flavor.id,
        networks=[{"uuid": network.id}], security_groups=security_groups, key_name=keypair.name)

    server = conn.compute.wait_for_server(server)

    print("ssh -i {key} ubuntu@{ip}".format(
        key=PRIVATE_KEYPAIR_FILE,
        ip=server.addresses[NETWORK_NAME][0]['addr']))
