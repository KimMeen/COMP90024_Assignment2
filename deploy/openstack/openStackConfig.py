IMAGE_NAME = "NeCTAR Ubuntu 18.04 LTS (Bionic) amd64"
# IMAGE_ID = "4c5b48a0-fb86-4f4f-a98b-81e3af15e2eb"
FLAVOR_NAME = "uom.mse.2c9g"
# FLAVOR_NAME = "uom.general.1c4g"
NETWORK_NAME = "qh2-uom-internal"
KEYPAIR_NAME = "cccAssi2"
SECURITY_GROUPS = ['all']
SSH_DIR = "./"
PRIVATE_KEYPAIR_FILE = "cccAssi2_private.pem"
VOLUMES_MAP = {}
VOLUMES_MAP["master"] = "0567ee0f-0829-4e41-8a95-870096b77f75"
VOLUMES_MAP["slave-1"] = "9cdc5081-9bac-4d3c-ac14-ef569f8ff4e0"
VOLUMES_MAP["slave-2"] = "b2df30e6-950c-48d5-8919-d6927516cea7"
VOLUMES_MAP["slave-3"] = "13bbd454-ec59-48aa-8c28-3380cc5e8c1e"
