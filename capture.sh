

tshark -n -i mon0 -T fields -e frame.time_epoch -e radiotap.channel.freq  -e wlan.bssid   -e wlan.ssid -e wlan_radio.signal_dbm  -a duration:6  type mgt subtype beacon > $1


