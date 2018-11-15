from miScale import MiScale

def on_data_received(scale):
    # Do stuff
    print(scale)

mac_addr = "c8:0f:10:bf:cc:66"  # Can be None or empty too
callback = on_data_received
send_only_stabilized_weight = False

MiScale(mac_addr, callback, send_only_stabilized_weight)