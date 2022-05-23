#!/bin/bash 
	

#Sincronizare one time 
#pi# apt install ntpdate
#pi# ntpdate 0.ro.pool.ntp.org

echo "#unixtime dBm(TX)"
while true; do 
	dbm=$(hcitool -i hci0 cmd 0x08 0x007| tail -n1 | awk '{printf("%d", "0x" $5);}')
	t=$(date "+%s.%N")
	sleep 0.6
	echo ${t} ${dbm}
done


