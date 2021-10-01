

## Capture filters for tshark and tcpdump 

- tshark uses capture filters[^1] and display filters [^2]
- capture filters decide at harvesting time which packets are saved,
  whereas display filters select from already captured packets which
  ones are shown
- display filters are easily generated in wireshark using 'Apply as
  filter' context menu of each packet. Also see [^5]
- for capture filters, valid wlan types are mgt, ctl and data.

### capture filters examples
- imported from [^3]
- `wlan type mgt` - capture only management frames
- `wlan type ctl` - capture only control frames
- `wlan type data`  - capture only data frames
- `wlan type mgt subtype beacon` - capture only beacon frames
- `wlan type mgt subtype deauth` - capture only deauth frames
- `wlan subtype probereq` - capture only probe requests
- `not wlan mgt` - do not capture management frame (i.e. capture data & control frames)
- `not wlan mgt subtype beacon` - capture all frames except beacon frames
- `wlan type mgt and (subtype beacon or subtype probe-req)` - capture only beacon  and probe request frames 
- `wlan type mgt and (subtype deauth or subtype disassoc)` - capture on deauthentication and disassocation frames
- `(wlan type data) or (wlan type ctl and (subtype rts or subtype cts))` - capture only data frames and RTS/CTS control frames

- recovered from [^4]
- `wlan host 00:11:22:33:44:55 and subtype beacon`
- `wlan dst host 00:11:22:33:44:55`
- Capture only management frames: `type mgt`
- Capture everything except control frames: `not type ctl`
- Capture data frames to/from mac address 04:1e:64:ea:c3:ef `wlan host
  04:1e:64:ea:c3:ef and type data`
- Management frames Valid subtypes are: assocreq, assocresp,
reassocreq, reassocresp, probereq, probresp, beacon, atim, disassoc,
auth and deauth
- Control frames Valid subtypes are: ps-poll, rts, cts, ack, cf-end
and cf-end-ack
- Data frames Valid subtypes are: data, data-cf-ack, data-cf-poll,
data-cf-ack-poll, null, cf-ack, cf-poll, cf-ack-poll, qos-data,
qos-data-cf-ack, qos-data-cf-poll, qos-data-cf-ack-poll, qos,
qos-cf-poll and qos-cf-ack-poll
- Capture only beacons: `subtype beacon`
- Capture everything except beacons: `not subtype beacon`
- Capture beacons, probe requests and probe responses:
  `subtype beacon or subtype probereq or subtype proberesp`
- Capture all frames except beacons, probe requests and probe responses:
  `not subtype beacon and not subtype probereq and not subtype proberesp`
- Capture beacons, probe requests and probe responses to/from host
  00:0c:f6:69:f8:69: `(wlan host 00:0c:f6:69:f8:69 and subtype beacon)
  or (wlan host 00:0c:f6:69:f8:69 and subtype probereq) or (wlan host
  00:0c:f6:69:f8:69 and subtype proberesp)` You can also use this
  capture filter: `wlan host 00:0c:f6:69:f8:69 and (subtype beacon or
  subtype probereq or subtype proberesp)`
- Capture probe requests from wlan host 00:0c:f6:69:f8:69 and probe
responses from wlan host: 00:24:2c:69:f8:69 `(wlan host
00:0c:f6:69:f8:69 and subtype probereq) or (wlan host
00:24:2c:69:f8:69 and subtype proberesp)`
- Capture beacons, probe requests and probe responses to/from host
00:0c:f6:69:f8:69 or to/from host 00:24:2c:69:f8:69: `(wlan host
00:0c:f6:69:f8:69 or wlan host 00:24:2c:69:f8:69) and (subtype beacon
or subtype probereq or subtype proberesp)`
- Capture all packets from wlan src 00:24:2c:69:f8:69 except beacons,
  probe requests and probe responses: `wlan src 00:24:2c:69:f8:69 and
  not subtype beacon and not subtype probereq and not subtype
  proberesp`
- Capture all association requests/responses, reassociation
  requests/responses, disassociation and (de)authentication frames and
  all eapols: `(subtype assocreq or subtype assocresp or subtype
  reassocreq or subtype reassocresp or subtype disassoc or subtype
  auth or subtype deauth) or (ether proto 0x888e)`
- Capture all eapols, association requests/responses, reassociation
requests/responses, disassociation and (de)authentication frames
to/from wlan host 00:0c:f6:69:f8:69 or wlan host 00:24:2c:69:f8:69:
`(wlan host 00:0c:f6:69:f8:69 or wlan host 00:24:2c:69:f8:69) and
(ether proto 0x888e or subtype assocreq or subtype assocresp or
subtype reassocreq or subtype reassocresp or subtype disassoc or
subtype auth or subtype deauth)`
- Capture all frames to/from wlan host 00:0c:f6:69:f8:69 or wlan host
 00:24:2c:69:f8:69: `wlan host 00:0c:f6:69:f8:69 or wlan host
 00:24:2c:69:f8:69`




[^1]: https://gitlab.com/wireshark/wireshark/-/wikis/CaptureFilters

[^2]: https://gitlab.com/wireshark/wireshark/-/wikis/DisplayFilters

[^3]: http://www.lovemytool.com/blog/2010/07/wireshark-wireless-display-and-capture-filters-samples-part-2-by-joke-snelders.html

[^4]: https://wifinigel.blogspot.com/2018/04/wireshark-capture-filters-for-80211.html

[^5]: https://semfionetworks.com/wp-content/uploads/2021/04/wireshark_802.11_filters_-_reference_sheet.pdf

