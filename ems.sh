#!/bin/bash



_base=/opt
_ems_base="${_base}/ems-public"
_ems_config_file=/etc/opnbaton/ems/conf.ini

function start {
  sudo apt-get install -y python-pip


  sudo pip install GitPython==1.0.1
  sudo pip install gitdb==0.6.4
  sudo pip install smmap==0.9.0
  sudo pip install stomp.py==4.1.2
  sudo pip install wsgiref==0.1.2
  sudo python /opt/ems-public
}

function stop {
   sudo kill $(ps aux | grep 'python\ /opt/ems-public' | awk '{print $2}')
}

function kill {
    sudo kill $(ps aux | grep 'python\ /opt/ems-public' | awk '{print $2}')
}

function end {
    sudo kill $(ps aux | grep 'python\ /opt/ems-public' | awk '{print $2}')
}
function usage {
    echo -e "EMS\n"
    echo -e "Usage:\n\t ./ems.sh <option>\n\t"
    echo -e "where option is"
    echo -e "\t\t * start"
    echo -e "\t\t * stop"
    echo -e "\t\t * kill"
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
        "kill" )
            kill ;;
        * )
            usage
            end ;;
    esac
done
