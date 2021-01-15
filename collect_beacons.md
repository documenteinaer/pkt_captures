

## Methods for collecting WiFi signal strength readings under Linux 

Signal strength (SS) between two devices are required for a variety of studies, measurements, or applications.  

### Beacons 
The 802.11 standard mandates each AP to send beacons periodically (by default every 120.4ms) with broadcast, so that any device may receive it, even if it is not associated to the AP. 
This is the easiest packet to harvest if one has access to these beacons in the driver. All drivers use these beacons internally, but may not send them up to the OS.  

#### monitor mode 
This is the preferred method to collect beacons, since the monitor mode has access to ALL packets received by the card. 
Commands should be issued as root, indicated below by the `# ` sign:

`# iw phy phy0 interface add mon0 type monitor flags control otherbss`

creates the monitor mode interface, flags permitting capture of protocol frames. The same physical card may also have a managed 
mode interface, for example wlan0 that gets associated to an AP. The monitor mode interface mon0 will stay on the same channel as the main interface wlan0, but will be able 
to capture all protocol packets on that channel, including frames from other APs.  

`# ifconfig mon0 up`
`# tcpdump -s0 -ni mon0 `

#### managed mode 

The next commands work without having to be connected to an AP, but they perform a complete scan, therefore take a few seconds (2.5s on a raspberry PI, Broadcom card; 4.5s on Intel 6300 Ultimate-n). 

`# iw dev wlan0 scan | egrep -B2 '(SSID|freq)' `

obtains SSID, frequency, and SS, but command may take 5 secodns, as it cycles through all channels

`# iwlist scan | egrep -B3 SSID`

similar 

When conected to an existing AP, it is possible to obtain some SS readings from the driver, albeit not 10 readings per second.  

`# iwconfig wlan0` should answer

    wlan0     IEEE 802.11  ESSID:"Precis-Guest"  
          Mode:Managed  Frequency:2.457 GHz  Access Point: AA:AA:AA:EE:EE:EE  
          Bit Rate=24 Mb/s   Tx-Power=31 dBm  
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Encryption key:off
          Power Management:on
          Link Quality=70/70  Signal level=-37 dBm  
          Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
          Tx excessive retries:1  Invalid misc:0   Missed beacon:0

therefore card is associated to the AP and the SS is available in user space. These values can be collected from the kernel using: 
`while true; do  grep wlan0 /proc/net/wireless; sleep 0.1; done`


#### adhoc mode 

### Probes 
The 802.11 standard mandates each AP to answer probe requests from stations that are not yet associated. 
Therefore any station can solicit a response from any AP, without any credentials, so that a SS reading can be obtained.  
Generally probe requests and probe responses are managed by the driver as part of the association and 
handoff process, and usually are not available in user space. 
(TODO: to be studied further)

### Packets

If one can control two machines for the purpose of measuring SS, it is possible to generate packets at high rate (thousands of packets per second) 
on one machine, and measure thei received SS on the other machine  

#### monitor mode 
