#!/bin/bash
_base=/opt/openbaton
_ems_base="${_base}/ems"
_ems_config_file=/etc/openbaton/ems/conf.ini

function start {
  sudo apt-get install -y python-pip
  sudo pip install -r requirements.txt
  sudo python $_ems_base
}

function stop {
   sudo kill $(ps aux | grep 'python\ $_ems_base/src' | awk '{print $2}')
}

function usage {
    echo -e "EMS\n"
    echo -e "Usage:\n\t ./ems.sh <option>\n\t"
    echo -e "where option is"
    echo -e "\t\t * start"
    echo -e "\t\t * stop"
}

if [ $# -eq 0 ]
   then
        usage
        exit 1
fi

declare -a cmds=($@)
for (( i = 0; i <  ${#cmds[*]}; ++ i ))
do
    case ${cmds[$i]} in
        "start" )
            start ;;
        "stop" )
            stop ;;
        * )
            usage
            end ;;
    esac
done
