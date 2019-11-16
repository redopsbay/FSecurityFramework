#!/bin/bash
#######################################################
#													  #
#													  #
#					FSECURITYFRAMEWORK				  #
#								  					  #
#													  #
#######################################################
TARGETFILE=main.py
USER_ID=1000
CURRENT_ID=$UID

if [ "$USER_ID" -eq "$CURRENT_ID" ]
then
	echo "Running FSecurityFramework"
	echo "starting mysql database service, msfrpcd, apache2 web-server and the fsecurityframework"
	#start the mysql-server-administrator.	start the msfrpcd daemon foreground and attaching the fsecurityframework program.
	sudo /etc/init.d/mysql start && sudo /etc/init.d/apache2 start && msfrpcd -P 'admin' -S -f -n -a 127.0.0.1 -p 55553 | sudo python3 $TARGETFILE -style plastique | echo "Press CTRL+C to exit"

else
	echo "Must be run as local user. Because msfprcd server should be run as local user. not root!"
	echo "But the script will ask you for your root password in able to start the fsecurityframework."
fi

sudo killall xterm
sudo /etc/init.d/mysql stop
sudo /etc/init.d/apache2 stop
sudo killall /bin/sh
