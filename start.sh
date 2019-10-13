#!/bin/sh


cd /opt/ICM/

/usr/bin/python main.py &

while [ "1" = "1" ]

do

	# do something
	sleep 1
done


