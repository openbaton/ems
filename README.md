  <img src="https://raw.githubusercontent.com/openbaton/openbaton.github.io/master/images/openBaton.png" width="250"/>
  
  Copyright © 2015-2016 [Open Baton](http://openbaton.org). 
  Licensed under [Apache v2 License](http://www.apache.org/licenses/LICENSE-2.0).


# Open Baton Element Management System

This project contains the sources of the Open Baton Element Management System (EMS). The EMS is an AMQP producer/consumer running as an agent inside the deployed VMs for executing the lifecycle events received from the Generic VNFM. After the EMS starts, it connects to the RabbitMQ server, subscribes to the queue with its name and sends register message to the specific register-queue attending further commands from the VNFM.
EMS receives requests like clone scripts from specific git repositories, update them and execute with the arguments that were sent within the message.

## Technical Requirements

* python 2.7 
* pika 0.10.0
* pythonGit
* git

## How to install EMS

The EMS is typically installed by the Generic VNFM. Those are the commands executed by the Generic VNFM (via user-data) while booting the VM for installing the EMS: 

```
    echo "Downloading EMS from internet"
    echo "deb http://get.openbaton.org/repos/apt/debian/ ems main" >> /etc/apt/sources.list
    wget -O - http://get.openbaton.org/public.gpg.key | apt-key add -
    apt-get update
    apt-get install git -y
    apt-get install -y ems-$EMS_VERSION
```

where EMS_VERSION has to be configured with the latest version number available. After the installation make sure you configure the conf.ini file correctly: /etc/openbaton/ems/conf.ini

## How to use EMS

For starting and stopping the EMS you can use the following commands: 
```
sudo service ems start to start
sudo service ems stop to stop
```

## Issue tracker

Issues and bug reports should be posted to the GitHub Issue Tracker of this project

# What is Open Baton?

OpenBaton is an open source project providing a comprehensive implementation of the ETSI Management and Orchestration (MANO) specification.

Open Baton is a ETSI NFV MANO compliant framework. Open Baton was part of the OpenSDNCore (www.opensdncore.org) project started almost three years ago by Fraunhofer FOKUS with the objective of providing a compliant implementation of the ETSI NFV specification. 

Open Baton is easily extensible. It integrates with OpenStack, and provides a plugin mechanism for supporting additional VIM types. It supports Network Service management either using a generic VNFM or interoperating with VNF-specific VNFM. It uses different mechanisms (REST or PUB/SUB) for interoperating with the VNFMs. It integrates with additional components for the runtime management of a Network Service. For instance, it provides autoscaling and fault management based on monitoring information coming from the the monitoring system available at the NFVI level.

## Source Code and documentation

The Source Code of the other Open Baton projects can be found [here][openbaton-github] and the documentation can be found [here][openbaton-doc] .

## News and Website

Check the [Open Baton Website][openbaton]
Follow us on Twitter @[openbaton][openbaton-twitter].

## Licensing and distribution
Copyright [2015-2016] Open Baton project

Licensed under the Apache License, Version 2.0 (the "License");

you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## Support
The Open Baton project provides community support through the Open Baton Public Mailing List and through StackOverflow using the tags openbaton.

## Supported by
  <img src="https://raw.githubusercontent.com/openbaton/openbaton.github.io/master/images/fokus.png" width="250"/><img src="https://raw.githubusercontent.com/openbaton/openbaton.github.io/master/images/tu.png" width="150"/>

[fokus-logo]: https://raw.githubusercontent.com/openbaton/openbaton.github.io/master/images/fokus.png
[openbaton]: http://openbaton.org
[openbaton-doc]: http://openbaton.org/documentation
[openbaton-github]: http://github.org/openbaton
[openbaton-logo]: https://raw.githubusercontent.com/openbaton/openbaton.github.io/master/images/openBaton.png
[openbaton-mail]: mailto:users@openbaton.org
[openbaton-twitter]: https://twitter.com/openbaton
[tub-logo]: https://raw.githubusercontent.com/openbaton/openbaton.github.io/master/images/tu.png

