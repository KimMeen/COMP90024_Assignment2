## COMP90024 Cluster and Clould Computing - Assignment2
```
Group 66
  |-- Minghong Gao ()
  |-- Ming Jin (947351)
  |-- Kangping Xue ()
  |-- Ziang Chen ()
  |-- Wenjin Li ()
```
### Overview
The repository contains codes for environment deployment, tweets harvesting, tweets analysis, and front-end web.
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

### Tweets Harvest

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
'Servers' defines the entry of the database and 'DB' contains the table name of raw tweets and output results.

Then we execute the `analyzer.py` by using MPI inside of the Docker Container:
```
mpirun --allow-run-as-root -np 8 -H master-node:2,slave-node-1:2,slave-node-2:2,slave-node-3:2 --mca btl_tcp_if_execlude docker0 python analyzer.py
```
After several hours, the analysis results will be stored in `results_latest` table inside of the CouchDB, as the figure shown below.
![results_latest](https://github.com/KimMeen/COMP90024_Assignment2/blob/master/docs/results_latest.PNG)
### Websites
