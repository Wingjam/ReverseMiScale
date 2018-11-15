import argparse
from collections import defaultdict
from bluepy.btle import Scanner, Peripheral, DefaultDelegate, ADDR_TYPE_RANDOM, BTLEException

from scale import Scale
from constants import AD_TYPES, UNITS

def MiScale(mac_addr, callback, send_only_stabilized_weight):

    class ScanDelegate(DefaultDelegate):

        def __init__(self):
            DefaultDelegate.__init__(self)
            self.last_rawData = defaultdict(str)


        def handleData(self, scale):
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
            elif (scale.rawData[0] & 0x0F) == 0x03: # Imperial pound
                scale.unit = UNITS.LBS
            elif (scale.rawData[0] & 0x0F) == 0x02: # MKS kg
                scale.unit = UNITS.KG
                scale.weight /= 2  # Convert chinese Catty to kg.
            else:
                scale.unit = UNITS.UNKNOWN

            # Callback
            if send_only_stabilized_weight:
                if scale.isStabilized:
                    callback(scale)
            else:
                callback(scale)


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
            if mac_addr:
                if dev.addr == mac_addr:
                    self.handleData(self.getScaleInfo(dev))
            else:
                for (adtype, desc, value) in dev.getScanData():
                    if adtype == AD_TYPES.COMPLETE_LOCAL_NAME and value == "MI_SCALE":
                            self.handleData(self.getScaleInfo(dev))


    scanner = Scanner().withDelegate(ScanDelegate())
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
