#/bin/bash

if [ -e '/usr/bin/msfrpcd' ]
then
	echo "[*] Launching msfrpcd daemon"
	msfrpcd -P 'admin' -S -f -n -a 127.0.0.1 -p 55553
else
	echo "[!] Error Launching msfrpcd daemon"
fi
