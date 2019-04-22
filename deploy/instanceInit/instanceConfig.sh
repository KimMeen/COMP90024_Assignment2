# install docker and couchdb
sudo apt-get update

sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common -y

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io -y

sudo docker pull couchdb:2.3.0

sudo mkdir -p /etc/systemd/system/docker.service.d
sudo vim.tiny /etc/systemd/system/docker.service.d/http-proxy.conf

sudo systemctl daemon-reload
sudo systemctl restart docker

sudo docker pull couchdb:2.3.0

node=172.26.37.209
masternode=172.26.37.209
othernodes=172.26.37.193,172.26.37.196,172.26.37.207

sudo docker run -d \
    -p 4369:4369 \
    -p 5984:5984 \
    -p 5986:5986 \
    -p 9100:9100 \
    -v /home/ubuntu/data:/opt/couchdb/data \
    couchdb:2.3.0
sleep 3

# get container ID
cont=`sudo docker ps -all | grep couchdb | cut -f1 -d' '`


sudo docker exec ${cont} \
      bash -c "echo \"-setcookie couchdb_cluster\" >> /opt/couchdb/etc/vm.args"
sudo docker exec ${cont} \
      bash -c "echo \"-name couchdb@${node}\" >> /opt/couchdb/etc/vm.args"

sudo docker restart ${cont}
sleep 3
user=admin
pass=admin
sudo curl -XPUT "http://${node}:5984/_node/_local/_config/admins/${user}" --data "\"${pass}\""
sudo curl -XPUT "http://${user}:${pass}@${node}:5984/_node/couchdb@${node}/_config/chttpd/bind_address" --data '"0.0.0.0"'



sudo curl -XPOST "http://${user}:${pass}@${masternode}:5984/_cluster_setup" \
      --header "Content-Type: application/json" \
      --data "{\"action\": \"enable_cluster\", \"bind_address\":\"0.0.0.0\", \
        \"username\": \"${user}\", \"password\":\"${pass}\", \"port\": \"5984\", \
        \"remote_node\": \"${node}\", \
        \"remote_current_user\":\"${user}\", \"remote_current_password\":\"${pass}\"}"

curl -XPOST "http://${user}:${pass}@${masternode}:5984/_cluster_setup" \
      --header "Content-Type: application/json" \
      --data "{\"action\": \"add_node\", \"host\":\"${node}\", \
        \"port\": \"5984\", \"username\": \"${user}\", \"password\":\"${pass}\"}"

curl -XPOST "http://${user}:${pass}@${masternode}:5984/_cluster_setup" \
    --header "Content-Type: application/json" --data "{\"action\": \"finish_cluster\"}" 


rev=`curl -XGET "http://${masternode}:5984/_nodes/nonode@nohost" --user "${user}:${pass}" | sed -e 's/[{}"]//g' | cut -f3 -d:`
curl -X DELETE "http://${masternode}:5986/_nodes/nonode@nohost?rev=${rev}"  --user "${user}:${pass}"