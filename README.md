# Reverse Mi Scale
Read [Xiaomi Mi Scale v1](http://www.mi.com/en/scale/) data from a Raspberry Pi in Python 3.

## Run 
1. Install dependencies
```
pip install -r requirements.txt
```

2. Run the demo (must be run with `sudo`)
```
sudo python example.py --help
sudo python example.py
```

3. Optionnal, if you want to find your Mi Scale MAC Address
```
sudo hcitool lescan
```

## Run tests
```
pytest
```

## Output samples
```json
{
    "UUID": "181d",
    "address": "c8:0f:10:bf:cc:66",
    "isStabilized": false,
    "loadRemoved": true,
    "manufacturerData": "5701c80f10bfcc66",
    "rawData": "820000e2070b0f082924",
    "sequence": 10532,
    "unit": "kg",
    "weight": 0.0
}
{
    "UUID": "181d",
    "address": "c8:0f:10:bf:cc:66",
    "isStabilized": true,
    "loadRemoved": false,
    "manufacturerData": "5701c80f10bfcc66",
    "rawData": "226455e2070b0f0c1d1b",
    "sequence": 7451,
    "unit": "kg",
    "weight": 109.3
}
{
    "UUID": "181d",
    "address": "c8:0f:10:bf:cc:66",
    "isStabilized": true,
    "loadRemoved": true,
    "manufacturerData": "5701c80f10bfcc66",
    "rawData": "a26455e2070b0f082a23",
    "sequence": 10787,
    "unit": "kg",
    "weight": 109.3
}
{
    "UUID": "181d",
    "address": "c8:0f:10:bf:cc:66",
    "isStabilized": false,
    "loadRemoved": false,
    "manufacturerData": "5701c80f10bfcc66",
    "rawData": "02e402b2080101010422",
    "sequence": 1058,
    "unit": "kg",
    "weight": 3.7
}
```

## Source of inspiration
* [Node Xiaomi Scale](https://github.com/perillamint/node-xiaomi-scale) (mostly)
* [Xiaomi Scale Scan](https://github.com/chaeplin/Xiaomi_scale_scan)
* [Xiaomi Mi Scale Reverse Engineering](https://github.com/oliexdev/openScale/wiki/Xiaomi-Bluetooth-Mi-Scale)
* [MiBand2](https://github.com/creotiv/MiBand2)

Thanks for providing those awesome open source projects.
