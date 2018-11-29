import argparse
from collections import defaultdict
from bluepy.btle import Scanner, Peripheral, DefaultDelegate, ADDR_TYPE_RANDOM, BTLEException

from scale import Scale
from constants import AD_TYPES, UNITS

class ScanDelegate(DefaultDelegate):
    def __init__(self, mac_addr, callback, send_only_stabilized_weight):
        DefaultDelegate.__init__(self)
        self.mac_addr = mac_addr
        self.callback = callback
        self.send_only_stabilized_weight = send_only_stabilized_weight
        self.last_rawData = defaultdict(str)


    def handleData(self, scale):
        # MiScale Raw Data Schema
        # +------+------------------------+
        # | byte |        function        |
        # +------+------------------------+
        # | 0    | Bit 0: unknown         |
        # |      | Bit 1: kg              |
        # |      | Bit 2: lbs             |
        # |      | Bit 3: unknown         |
        # |      | Bit 4: jin unit        |
        # |      | Bit 5: stabilized      |
        # |      | Bit 6: unknown         |
        # |      | Bit 7: load removed    |
        # +------+------------------------+
        # | 1-2  | weight (little endian) |
        # +------+------------------------+
        # | 3-7  | unknown                |
        # +------+------------------------+
        # | 8-9  | sequence (big endian)  |
        # +------+------------------------+

        # Check for duplicate packet
        if scale.rawData == self.last_rawData[scale.address]: return
        
        # Update duplication lookup table
        self.last_rawData[scale.address] = scale.rawData

        scale.isStabilized = (scale.rawData[0] & (1<<5)) != 0
        scale.loadRemoved = (scale.rawData[0] & (1<<7)) != 0

        scale.weight = int.from_bytes(scale.rawData[1:3], byteorder='little') / 100
        scale.sequence = int.from_bytes(scale.rawData[8:10], byteorder='big')

        # Unit
        if (scale.rawData[0] & (1<<4)) != 0: # Chinese Catty
            scale.unit = UNITS.JIN
        elif (scale.rawData[0] & (1<<2)) != 0: # Imperial pound
            scale.unit = UNITS.LBS
        elif (scale.rawData[0] & (1<<1)) != 0: # MKS kg
            scale.unit = UNITS.KG
            scale.weight /= 2  # Convert chinese Catty to kg.
        else:
            scale.unit = UNITS.UNKNOWN

        # Callback
        if self.send_only_stabilized_weight:
            if scale.isStabilized:
                self.callback(scale)
        else:
            self.callback(scale)


    def getScaleInfo(self, dev):
        scale = Scale(address=dev.addr)
        
        for (adtype, desc, value) in dev.getScanData():
            if adtype == AD_TYPES.SERVICE_DATA:
                scale.UUID = bytes.fromhex(value[0:4])[::-1].hex()
                scale.rawData = bytes.fromhex(value[4:])
            elif adtype == AD_TYPES.MANIFACTURER:
                scale.manufacturerData = bytes.fromhex(value)
        return scale


    def handleDiscovery(self, dev, isNewDev, isNewData):
        if self.mac_addr:
            if dev.addr.upper() == self.mac_addr:
                self.handleData(self.getScaleInfo(dev))
        else:
            for (adtype, desc, value) in dev.getScanData():
                if adtype == AD_TYPES.COMPLETE_LOCAL_NAME and value == "MI_SCALE":
                        self.handleData(self.getScaleInfo(dev))

def MiScale(mac_addr, callback, send_only_stabilized_weight):
    mac_addr = mac_addr.upper()
    scanner = Scanner().withDelegate(ScanDelegate(mac_addr, callback, send_only_stabilized_weight))
    while True:
        scanner.start()
        scanner.process(1)
        scanner.stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Display Xiaomi scale data.')
    parser.add_argument("-a", "--address", help="The specific scale MAC address to retreive data. If not provided, match any Xiaomi scale")
    parser.add_argument("-s", "--stabilized", action="store_true", help="Send only data when the weight is stabilized")
    args = parser.parse_args()

    # When called from console, print directly the scale data
    MiScale(args.address, print, args.stabilized)
