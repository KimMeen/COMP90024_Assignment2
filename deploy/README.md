# Environment and Configuration

This repo includes configuration scripts. Deployment is achieved with the help of provisioning tools(boto3 and ansible).

## Prerequisite
1. Python3, boto3(pip install boto3), ansible(pip install ansible) should be installed.
2. grep is not fully supported on Mac-OS. gnu-grep can be installed easily using homebrew. Remember to add to path.
3. RSA key-pair exactly named as "assi2-key" must be generated on local machine(using following commands) and should be added to NeCTAR
```
ssh-keygen -t rsa -f assi2-key -m PEM
ssh-agent bash; ssh-add ~/.ssh/assi2-key
```
4. Security Group called "couchdb" should be created on NeCTAR. Ingress TCP Port 5984
