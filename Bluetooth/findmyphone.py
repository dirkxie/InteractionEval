import bluetooth
import bluetooth._bluetooth as bluez
import struct

#target_name = "My Phone"
target_address = None

dev_id = 0
sock = bluez.hci_open_dev(dev_id)
# save current filter
old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)

# perform a device inquiry on bluetooth device #0
# The inquiry should last 8 * 1.28 = 10.24 seconds
# before the inquiry is performed, bluez should flush its cache of
# previously discovered devices
flt = bluez.hci_filter_new()
bluez.hci_filter_all_events(flt)
bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )

duration = 4
max_responses = 255
cmd_pkt = struct.pack("BBBBB", 0x33, 0x8b, 0x9e, duration, max_responses)
bluez.hci_send_cmd(sock, bluez.OGF_LINK_CTL, bluez.OCF_INQUIRY, cmd_pkt)


nearby_devices = bluetooth.discover_devices()

for bdaddr in nearby_devices:

    #if target_name == bluetooth.lookup_name( bdaddr ):
        #target_address = bdaddr
        #break
    pkt = sock.recv(255)
    rssi = bluetooth.byte_to_signed_int(bluetooth.get_byte(pkt[1+13*nrsp+i])) 
    print bdaddr 

#if target_address is not None:
    #print "found target bluetooth device with address ", target_address
#else:
    #print "could not find target bluetooth device nearby"

