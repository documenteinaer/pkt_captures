#!/usr/bin/env python3

duration = 4 # seconds 
# ./capture.py > out.json 2> log.txt 
#

import shlex, subprocess, sys
import json
from sys import platform
#import numpy as np
from datetime import datetime


if(platform=="linux"):
    # check if mon0 is present 
    tshark_params="tshark -n -i mon0 -T fields -e frame.time_epoch -e radiotap.channel.freq  -e wlan.bssid   -e wlan.ssid -e wlan_radio.signal_dbm  -a duration:%d  type mgt subtype beacon" % duration


if(platform == "darwin"): 
    tshark_params='/usr/local/bin/tshark -a duration:%d -Ini en1 -T fields -e frame.time_epoch -e wlan.bssid -e wlan_radio.signal_dbm type mgt subtype beacon' % duration

print(tshark_params, file=sys.stderr)

tshark = subprocess.Popen(shlex.split(tshark_params), stdout=subprocess.PIPE)
out, err = tshark.communicate()

collections = {}
collection = {}
fingerprints = []
fingerprint = {}
wifis = {}
now = datetime.now() 
date_time = now.strftime("%d-%m-%Y %H:%M:%S")

wifi_data = {}
wifi_data['rssi'] = []
for x in out.splitlines():
    pkt = x.decode().split('\t')
    wifi_data['ssid'] = pkt[3]
    wifi_data['frequency'] = pkt[1]
    wifi_data['rssi'].append(int(pkt[4]))
    hw_addr = pkt[2]
    wifis[hw_addr] = wifi_data
    print(pkt, file=sys.stderr)
    
fingerprint['timestamp'] = date_time
fingerprint['wifi'] = wifis
fingerprints.append(fingerprint)
collection['fingerprints'] = fingerprints
collections['collection0'] = collection 
    
json_collections = json.dumps(collections, indent=2)
print(json_collections)

