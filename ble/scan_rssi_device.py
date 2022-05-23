import argparse
import time
import re
from datetime import datetime
from bluepy.btle import Scanner, DefaultDelegate

parser = argparse.ArgumentParser(description="Scan beacons from a particular device and get its RSSI values.")
parser.add_argument('-a', '--mac-address', type=str, help='MAC address of the target device')

args = parser.parse_args()

fn = 'data/ble_data_' + datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S') + '.csv'
with open(fn, 'w') as f:
    f.write('ts,mac,rssi\n')


# create a delegate class to receive the BLE broadcast packets
class ScanDelegate(DefaultDelegate):

    def __init__(self):
        DefaultDelegate.__init__(self)

        self.acc_rssi = 0
        self.cnt_rssi = 0
        self.nr_samples = 20

    # when this python script discovers a BLE broadcast packet, print a message with the device's MAC address
    def handleDiscovery(self, dev, isNewDev, isNewData):
        #if dev.addr.upper() == args.mac_address.upper():
        ts = time.time()
        ts_format = datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')

        isKontakt = re.search(b'Kontakt', dev.rawData) #.decode('utf-8'))
        if isKontakt: # dev.addr.upper() == args.mac_address.upper():
            print('{} Received message from {} with RSSI {}, data {}'.format(ts_format, dev.addr, dev.rssi, dev.rawData))
            #print(dev))
            #for k in keys(dev):
            #    print(k)
                
            with open(fn, 'a') as f:
                f.write('{},{},{}\n'.format(ts, dev.addr, dev.rssi))

            self.acc_rssi += dev.rssi
            self.cnt_rssi += 1

            if self.cnt_rssi >= self.nr_samples:
                print('Average RSSI: ', self.acc_rssi / self.cnt_rssi)
                self.acc_rssi = 0
                self.cnt_rssi = 0

        #else:
        #print('{} Received message from {} with RSSI {}, count {}'.format(ts, dev.addr, dev.rssi, dev.updateCount))

# create a scanner object that sends BLE broadcast packets to the ScanDelegate
scanner = Scanner().withDelegate(ScanDelegate())

THRESH = 1 # seconds


ts_start = time.time()
scanner.start()

# start the scanner and keep the process running
while True:
    if time.time() - ts_start < THRESH:
        err = scanner.process(timeout=1)
        print('continue...')
    else:
        ts_start = time.time()
        scanner.stop()
        scanner.clear()
        scanner.start()
        print('Restarted scanner, delay = ', time.time() - ts_start)

