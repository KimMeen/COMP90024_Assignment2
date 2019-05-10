### Analysis part: Docker configuration [In Chinese]


首先在四个nodes上下载镜像文件：
```
sudo docker pull mingj2/horovod_py3.5 
```

然后使用如下命令在四个nodes上运行container：
```
以Master node为例
sudo nvidia-docker run -h MasterNode -it --network=host -v /mnt:/mnt mingj2/horovod_py3.5:v1.0
```

分别进入各个nodes下的container中，修改ssh细则：
```
vim /etc/ssh/ssh_config
  -- 修改 RSAAuthentication yes
  -- 修改 PasswordAuthentication yes
  -- 修改 IdentityFile ~/.ssh/identity
  -- 修改 IdentityFile ~/.ssh/id_rsa

再vim /etc/ssh/sshd_config
  -- 修改 Port 22 为 1234
  -- 修改 PermitRootLogin 为 yes
```

现在配置各节点免密码访问：
```
请参考这个教程：http://www.linuxproblem.org/art_9.html
```

设置好后配置/root/.ssh/config文件：
```
vim /root/.ssh/config

修改成这样，以master node为例：
Host MasterNode
   Hostname <IP Address here>
   Port 1234
   User root
Host Slave1
   Hostname <IP Address here>
   Port 1234
   User root
...
```

现在请互相ssh验证：
```
以master node为例
ssh Slave1
ssh Slave2
...
```

如果没有问题，运行一个MPI例子，比如这个：
```
import mpi4py.MPI as MPI

comm = MPI.COMM_WORLD
comm_rank = comm.Get_rank()
comm_size = comm.Get_size()

data = [1,2,3,4]

local_data = comm.scatter(data, root=0)

print('I am rank:', comm_rank, ' and I got:', local_data)
```


运行命令：
```
mpirun --allow-run-as-root -np 4 -H MasterNode:1,Slave1:1,Slave2:1,Slave3:1 -mca btl_tcp_if_exclude docker0 python /mnt/mpitester.py
```

运行结果应该是这样的：
```
I am rank: 0  and I got: 1
I am rank: 1  and I got: 2
I am rank: 2  and I got: 3
I am rank: 3  and I got: 4
```

教程结束！
