In order to test EMS without virtual network function manager, the messages in json format should be passed
to ActiveMQ server directly to the queue, to which EMS is subscribe. The format would be vnfm-<hostname of the ems>-actions.
The hostname can be changed in the /etc/openbaton/ems/conf.ini file along with the ip and port of the activemq. By default these are localhost and 61613.
Default hostname is newName1. The further steps are following:

1. Start EMS.
2. Open ActiveMQ GUI through your internet browser and locate the queue with the the name vnfm-<hostname of the ems>-actions.
3. Find the words "Send To" at the end of the line and press it.
4. On the opened page, type in or copy json commands you would like to test into the "message body" field.
5. Press Send.

After this EMS will pick the message off the queue and process in accordingly.
The examples of the current messages EMS might process are:

{"action":"SAVE_SCRIPTS", "payload":"d29uZGVycw==", "name":"Example_script", "script-path":"/opt/savedscripstest"}
{"action":"SAVE_SCRIPTS", "payload":"d29uZGVycw==", "name":"Example_script"}
{"action":"EXECUTE", "payload":"test.sh argument1"}
