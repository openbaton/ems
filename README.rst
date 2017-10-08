Open Baton Element Management System for Generic VNFM
====================================
  
This project contains the sources of the Open Baton Element Management System (EMS). The EMS is an AMQP producer/consumer running as an agent inside the deployed VMs for executing the lifecycle events received from the Generic VNFM. After the EMS starts, it connects to the RabbitMQ server, subscribes to the queue with its name and sends register message to the specific register-queue attending further commands from the VNFM.
EMS receives requests like clone scripts from specific git repositories, update them and execute with the arguments that were sent within the message.

Technical Requirements
----------------------

- python 2.7 
- pika 0.10.0
- pythonGit
- git
- python pip

How to install the Open Baton EMS
---------------------------------
The EMS is typically installed by the Generic VNFM. Those are the commands executed by the Generic VNFM (via user-data) while booting the VM for installing the EMS: 

.. code:: bash

            apt-get install -y python-pip
            pip install --upgrade pip
            pip install pika
            pip install gitpython
            cp /usr/share/zoneinfo/$TIMEZONE /etc/localtime
            apt-get install -y git
            mkdir /opt/openbaton
            pip install openbaton-ems
            add-upstart-ems
            
After the installation make sure you configure the conf.ini file correctly: /etc/openbaton/ems/conf.ini

How to use EMS
---------------------------------

For starting EMS

.. code:: bash

              openbaton-ems
         
For adding EMS to upstart job and services list. Currently works on Ubuntu and Centos 7

.. code:: bash

              add-upstart-ems

Issue tracker
-------------

Issues and bug reports should be posted to the GitHub Issue Tracker of this project

What is Open Baton?
===================

Open Baton is an open source project providing a comprehensive implementation of the ETSI Management and Orchestration (MANO) specification and the TOSCA Standard. Open Baton provides multiple mechanisms for interoperating with different VNFM vendor solutions. 
It has a modular archiecture which can be easily extended for supporting additional use cases. 

It integrates with OpenStack as standard de-facto VIM implementation, and provides a driver mechanism for supporting additional VIM types. It supports Network Service management either using the provided Generic VNFM and Juju VNFM, or integrating additional specific VNFMs. It provides several mechanisms (REST or PUB/SUB) for interoperating with external VNFMs. 

It can be combined with additional components (Monitoring, Fault Management, Autoscaling, and Network Slicing Engine) for building a unique MANO comprehensive solution.

Source Code and documentation
-----------------------------

The Source Code of the other Open Baton projects can be found
`here <http://github.org/openbaton>`__ and the documentation can be
found `here <http://openbaton.org/documentation>`__ .


News and Website
----------------

Check the `Open Baton Website <http://openbaton.org>`__ Follow us on
Twitter @\ `openbaton <https://twitter.com/openbaton>`__.

Licensing and distribution
--------------------------

Copyright [2015-2016] Open Baton project

Licensed under the Apache License, Version 2.0 (the "License");

you may not use this file except in compliance with the License. You may
obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Copyright © 2015-2016 `Open Baton <http://openbaton.org>`__. Licensed
under `Apache v2 License <http://www.apache.org/licenses/LICENSE-2.0>`__.

Support
-------

The Open Baton project provides community support through the Open Baton
Public Mailing List and through StackOverflow using the tags openbaton.

Supported by
------------

.. image:: https://raw.githubusercontent.com/openbaton/openbaton.github.io/master/images/fokus.png
   :width: 250 px

.. image:: https://raw.githubusercontent.com/openbaton/openbaton.github.io/master/images/tu.png
   :width: 250 px
