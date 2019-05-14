#!/bin/bash
cd ./openstack
printf "\n" >> ../ansible/hosts.ini

echo "[Master-Node]" >> ../ansible/hosts.ini
python2 ./openStackCreate.py openstack_group master-node
printf "\n" >> ../ansible/hosts.ini

echo "[Slave-Nodes]" >> ../ansible/hosts.ini
python2 ./openStackCreate.py openstack_group slave-node-1
python2 ./openStackCreate.py openstack_group slave-node-2
python2 ./openStackCreate.py openstack_group slave-node-3
printf "\n" >> ../ansible/hosts.ini
chmod +x ./auth.sh
source ./auth.sh
# Volumes 
`python2 ./openStackAttachVolume.py master-node master`
`python2 ./openStackAttachVolume.py slave-node-1 slave-1`
`python2 ./openStackAttachVolume.py slave-node-2 slave-2`
`python2 ./openStackAttachVolume.py slave-node-3 slave-3`

sleep 90s
export ANSIBLE_HOST_KEY_CHECKING=False


cd ../ansible
ansible-playbook play_book.yaml -i ./hosts.ini
