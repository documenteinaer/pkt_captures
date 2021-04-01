#!/bin/sh 

#channel changing works only when main card is not associated
#mon0 needs to be up 

ifconfig wlp2s0 down
ifconfig mon0 up 

f_1_6_11="2412 2437 2462"
f_5GHz_indoor="5180 5200 5220 5240 5260 5280 5300 5320"
f_5GHz_outdoor="5500 5520 5540 5560 5580 5600 5620 5640 5660 5680 5700"
f_5GHz_all="$f_5GHz_indoor $f_5GHz_outdoor"

#PRECIS 
#freq="2412 2437 2462 5180 5200 5220 5240 5260 5280 5320"

#Mumu 
freq="$f_1_6_11 5180 5200 5240"

if [ "x$1x" = "xx" ]; then
    max=10000000
else
    max=$1
fi
count=0

while [ $count -lt $max ]; do
    for f in $freq; do 
	iw dev mon0  set freq $f
	echo $f
	sleep 0.5
    done
    count=$(($count+1))
done

