

#
# Only for certain phones with Qualcomm wifi chip 
# WiFi needs to be turned off 
#

if [ $# -lt 1 ]; then 
    echo "$0  on|off"
    exit 1
elif [ $1 == "on" ]; then 
    ip l s wlan0 down
    echo 4 >  /sys/module/wlan/parameters/con_mode
    sleep 1
    ip l s wlan0 up
    iw wlan0 set channel 64
    # tcpdump -ni wlan0 -s0
elif [ $1 == "off" ]; then 
    ip l s wlan0 down
    echo 0 >  /sys/module/wlan/parameters/con_mode
    sleep 1
    ip l s wlan0 up
fi


