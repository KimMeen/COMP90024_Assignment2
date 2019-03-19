#!/bin/bash

cat ./ansible/hosts_default > ./ansible/hosts


#Append Master Node to Ansible hosts
echo "Creating Node 1..."
echo -e "\n[node1-master]" >> ./ansible/hosts
python3 ./boto3/create_instance.py |grep -Po '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}' >> ./ansible/hosts
echo "Node 1 Master instance created"

#Append Slave Node to Ansible hosts
echo "Creating Node 2..."
echo -e "\n[node2-slave]" >> ./ansible/hosts
python3 ./boto3/create_instance.py |grep -Po '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}' >> ./ansible/hosts
echo "Node 2 Slave instance created"
