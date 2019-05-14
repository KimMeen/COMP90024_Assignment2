## COMP90024 Cluster and Clould Computing - Assignment2
```
Group 66
  |-- Minghong Gao (798106)
  |-- Ming Jin (947351)
  |-- Kangping Xue (878962)
  |-- Ziang Chen (957348)
  |-- Wenjin Li (931352)
```
### Overview
The repository contains codes for environment deployment, tweets harvesting, tweets analysis, and front-end web.

Website : http://172.26.38.167:8080/index


Video: https://www.youtube.com/watch?v=sPc_wLi9gKI&feature=youtu.be

```
master
  |-- Server: This folder contains codes related to front-end webs
  |-- analysis: This folder contains codes related to sentiments and topics analysis
  |-- deploy: This folder contians codes related to environment configuration (e.g., Ansible and Docker)
  |-- docs: This folder contains some sceenshots and related documents
  |-- harvester: This folder contains codes related to tweets harvesting
  |-- util: This folder contains some general tools, such as tweets preprocessing
```

### Deployment
```
chmod -x deploy.sh

git clone git@github.com:KimMeen/COMP90024_Assignment2.git

cd ./deploy

./deploy.sh
```

### Tweets Harvest
To run the tweets harvset, be sure to include twitter_config.py and harvester under a same directory, the run command：
```
python3 harvester.py
```

### Analysis
Firstly, we predefine the CouchDB configuration file (db_config.json) under ./analysis directory:
```
{
   "Servers":[
      "http://admin:admin@127.0.0.1:5984/"
   ],
   
   "DB":[
       "tweets",
       "results_latest"
   ]
}
```
'Servers' defines the entry of the CouchDB server and 'DB' contains the DB name of documents produced by harvester and analyzer.

Then we execute the `analyzer.py` by using MPI inside of the Docker Container:
```
mpirun --allow-run-as-root -np 8 -H master-node:2,slave-node-1:2,slave-node-2:2,slave-node-3:2 --mca btl_tcp_if_execlude docker0 python analyzer.py
```
After several hours, the analysis results will be stored in `results_latest` table inside of the CouchDB, as the figure shown below.
![results_latest](https://github.com/KimMeen/COMP90024_Assignment2/blob/master/docs/results_latest.PNG)

### Websites
The Web Server uses flask web framework. There are serveral options for user to deploy/run the appliation on their local development server. In default, the application has specified a app.run method to start the Server. On command line, simply `python3 Server db_address` or `nohup python3 Server db_adderss` to keep the server running on the background where db_address is the database address for the server
```
app.run('0.0.0.0', port, debug, options)
debug : defaults to false. If set to true, provides a debug information
options : to be forwarded to underlying Werkzeug server.
```
However, flask’s built-in server is not suitable for production as it doesn’t scale well. If user uses the hosted option to deploy the server for example Heroku, OpenShift, Google App Engine etc. Please refer the below link http://flask.pocoo.org/docs/1.0/deploying/ 
