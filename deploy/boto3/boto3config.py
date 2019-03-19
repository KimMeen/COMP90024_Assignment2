# EC2 Config
ACCESS_KEY = "5edea38a42544f7cb97c377d66a1cc2e"
SECRET_KEY = "f3fa2ab2cddd4eed87f5246be5b89aeb"
DEFAULT_REGION = "RegionOne"
EC2_ENDPOINT_URL = "https://nova.rc.nectar.org.au:8773/services/Cloud"

# Instance Detail Config
IMAGE_ID="ami-f70a8026"
INSTANCE_ID="node-1-master"
INSTANCE_TYPE="m2.small"
SECURITY_GROUPS=["SSH","couchdb"]
PLACEMENT="melbourne-qh2"
KEY_NAME="assi2-key"
MAX_COUNT=2
MIN_COUNT=1

# create ssh as pem format
# ssh-keygen -t rsa -f assi2-key -m PEM
# ssh-agent bash; ssh-add ~/.ssh/assi2-key
