#!/bin/bash

function usage(){
	echo usage: $0 version 
}

if [ $# -eq 0 ]
   then
        usage
        exit 1
fi

version=$1

dpkg-deb --build ems ems-$version.deb

