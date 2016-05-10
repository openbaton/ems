# Element Management System
------


### Prerequisites

* python 2.7 
* pika 0.10.0
* pythonGit
* git

### Usage

sudo service ems start to start
sudo service ems stop to stop

### conf.ini

Inside the folder etc there is a configuration file, conf.ini, where parameteres are stored



Element Management System works by getting the commands from orchestrator through the manager. It is supposed to control the virtual network funktion. It receives its commands throught the broker(RabbitMQ server).
After the EMS starts, it connects to rabbitemq-server, subscribes to the queue with its name and sends register message to the specific register-queue on the server.
EMS waits for the messages in json-format and executes them on arrival. It can clone scripts from repository, update them and execute with the arguments that were sent with the message. 

