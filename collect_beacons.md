

## Methods for collecting WiFi signal strength readings under Linux 

Signal strength (SS) between two devices are required for a variety of studies, measurements, or applications.  
SS is available in each packet in monitor mode, but many cards do not support monitor mode, or it is undocumented. 
When monitor mode is not available, some SS readings are still available to the kernel, and are accessible in user space with utilities such as `iw, iwconfig, iwlist`, 
or directly as a reading in `proc/net/wireless`. There are several methods to gather SS, but they differ with respect to: driver availability, frequency of collection, type of packets collected, possibility to generate packets at the source. 

### Beacons 
The 802.11 standard mandates each AP to send beacons periodically (by default every 102.4ms) with broadcast, so that any device may receive it, even if it is not associated to the AP. 
This is the easiest packet to harvest if one has access to these beacons in the driver. All drivers use these beacons internally, but may not send them up to the OS.  

#### monitor mode 
This is the preferred method to collect beacons(or any other packets), since the monitor mode has access to ALL packets received by the card. 
Commands should be issued as root, indicated below by the `# ` sign:

`# iw phy phy0 interface add mon0 type monitor flags control otherbss`

creates the monitor mode interface, flags permitting capture of protocol frames. The same physical card may also have a managed 
mode interface, for example wlan0 that gets associated to an AP. The monitor mode interface mon0 will stay on the same channel as the main interface wlan0, but will be able 
to capture all protocol packets on that channel, including frames from other APs.  

`# ifconfig mon0 up`
`# tcpdump -s0 -ni mon0 ` captures all packets from the interface 

`# tshark -T fields -e frame.time_epoch -e radiotap.channel.freq  -e wlan.bssid   -e wlan.ssid -e radiotap.dbm_antsignal  -s0 -ni mon0   type mgt subtype beacon` captures only beacon frames 

tshark has the same [capture syntax](https://wiki.wireshark.org/CaptureFilters) as tcpdump, but has a separate [display syntax](https://wiki.wireshark.org/DisplayFilters), which  is the one from wireshark. In the above example, we capture beacons and only print a few 
fields: time, frequency, AP address, SSID, and signal strength for the beacon. More [802.11 capture options](https://wifinigel.blogspot.com/2018/04/wireshark-capture-filters-for-80211.html).  

`# tshark   -s0 -ni mon0  link[0] == 0x80` both tcpdump/tshark can capture based on individual bytes in the header. This filter selects only beacon frames.

`# tcpdump -s0 -ni mon0 -w ./saved.pcap` both tshark/tcpdump can save packets in a file that can later be inspected with tshark (or wireshark, which is more instructional for the protocol fields and print syntax)

`# tshark -T fields -e frame.time_epoch -e wlan.bssid -e radiotap.dbm_antsignal -r ./saved.pcap '(wlan.fc.type_subtype == 0x0008) && (wlan.bssid == 22:22:22:11:11:11)'` use a selection filter to select beacon frames from the file, and only prints certain fields. Here we see the display filter syntax, which is also used by wireshark.   

Raspberry PIs unfortunately do nos support monitor mode out of the box, as they rely on Broadcom chipsets :-(. There seems to be a way to patch the kernel to allow for [monitor mode on the Pi](https://github.com/seemoo-lab/nexmon).    

#### managed mode - not connected 

The next commands work without having to be connected to an AP, but they perform a complete scan, therefore take a few seconds (2.5s on a raspberry PI, Broadcom card; 4.5s on Intel 6300 Ultimate-n). 

`# iw dev wlan0 scan | egrep -B2 '(SSID|freq)' `

obtains SSID, frequency, and SS, but command may take 5 seconds, as it cycles through all channels

`# iwlist scan | egrep -B3 SSID`

similar 

#### managed mode - connected 

When conected to an existing AP, it is possible to obtain some SS readings from the driver, albeit not 10 readings per second.  

To connect a raspberry Pi, we put these lines in /etc/network/interfaces:

    auto wlan0
    iface wlan0 inet dhcp
    #  address 10.2.0.2
    #  netmask 255.255.255.0
    #  wireless-channel 6
    wireless-essid UPB-Guest
    wireless-mode managed

and run `# /etc/init.d/networking restart` to get the card connected to an existing AP without password.  

An alternate method if there is not another type of network manager running is to use the 
command `# iwconfig wlan0 essid UPB-Guest` which will associate, but not obtain an IP address. 

To verify that card is successfully associated, run: 

`# iwconfig wlan0` should answer

    wlan0 IEEE 802.11  ESSID:"UPB-Guest"  
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

For these commands we are not actually getting IP datapackets from the AP, but collect SS from the beacons received and reported to the kernel.   
This method is convenient because it does not require setting up the IP link for the client, which involves dhcp, routing, possibly NAT, etc. 

#### adhoc mode 

TODO 

### Probes 
The 802.11 standard mandates each AP to answer probe requests from stations that are not yet associated. 
Therefore any station can solicit a response from any AP, without any credentials, so that a SS reading can be obtained.  
Generally probe requests and probe responses are managed by the driver as part of the association and 
handoff process, and usually are not available in user space. 

tcpdump/tshark capture filter: 
`# tcpdump -s0 -ni mon0 type mgt subtype probe-resp or subtype probe-req`

TODO: 
 - probe collection in Android 
 - probe requests 
 - scapy 

### Packets

If one can control two machines for the purpose of measuring SS, it is possible to generate packets at high rate (thousands of packets per second) 
on one machine, and measure thei received SS on the other machine. For this method it is necessary to have IP properly set up between the AP (or a machine behind the AP) and the client. It then comes down to the question of what software can be installed on the endpoints to generate/receive traffic.   

#### ping 

An easy way to generate broadcast packets is using `# ping -b`. These packets do not wait for 802.11 ACKs, and are not retried, therefore are a good candidate 
to use as a simple probing packet. 


#### iperf 

iperf can generate UDP traffic and has options for: packet rate, packet size, destination address. 

#### monitor mode 
