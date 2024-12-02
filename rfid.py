# import for GPIO--------------------------------------------
import wiringpi
from time import sleep
# import for RFID--------------------------------------------
import logging
import threading
logger = logging.getLogger(__name__)
import usb.core
import usb.util
import usb.backend.libusb1
from request_server import push_server
import time

import csv
stop_event = threading.Event()
# ---------------------------------------------------------------
wiringpi.wiringPiSetup()
wiringpi.pinMode(6, 1)  # Set pin 6 to 1 ( OUTPUT )
# wiringpi.digitalWrite(6, 1)  # Write 1 ( HIGH ) to pin 6
# wiringpi.digitalRead(6)      # Read pin 6
# ---------------------------------------------------------------
debug = False
hid = {4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm',
       17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y',
       29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0', 40: '\n',
       44: ' ', 45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 51: ';', 52: '\'', 53: '~', 54: ',', 55: '.', 56: '/'}
hid2 = {4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G', 11: 'H', 12: 'I', 13: 'J', 14: 'K', 15: 'L', 16: 'M',
        17: 'N', 18: 'O', 19: 'P', 20: 'Q', 21: 'R', 22: 'S', 23: 'T', 24: 'U', 25: 'V', 26: 'W', 27: 'X', 28: 'Y',
        29: 'Z', 30: '!', 31: '@', 32: '#', 33: '$', 34: '%', 35: '^', 36: '&', 37: '*', 38: '(', 39: ')', 40: '\n',
        44: ' ', 45: '_', 46: '+', 47: '{', 48: '}', 49: '|', 51: ':', 52: '"', 53: '~', 54: '<', 55: '>', 56: '?'}
with open("/home/orangepi/RFID/Database.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    print('Database:')
    for row in reader:
        print(row)


def decode(data):
    try:
        if data[0] == 0:
            return hid[data[2]]
        if data[0] == 2:
            return hid2[data[2]]
    except KeyError:
        return '?'


def read_rfid():
    idVendor = 0xffff
    idProduct = 0x0035
    _backend = usb.backend.libusb1.get_backend()
    dev = usb.core.find(idVendor=idVendor, idProduct=idProduct, backend=_backend)
    if dev is None:
        logger.error('configured device is not connected {idVendor:s}:{idProduct:s}'.format(
            idVendor=self.parameters['usb.idVendor'], idProduct=self.parameters['usb.idProduct']))
        devices = usb.core.find(find_all=True, backend=_backend)
        for p in devices:
            logger.error("available device 0x{idVendor:04x}:0x{idProduct:04x}".format(idVendor=p.idVendor,
                                                                                      idProduct=p.idProduct))
        logger.error("check configuration file")
        return
    interface = 0
    endpoint = dev[0][(0, 0)][0]
    if debug:
        logger.info("wMaxPacketSize {ps:d}".format(ps=endpoint.wMaxPacketSize))
    if dev.is_kernel_driver_active(interface) is True:
        dev.detach_kernel_driver(interface)
        usb.util.claim_interface(dev, interface)
    result = ''
    count = 0
    tagid = ''

    while not stop_event.is_set():
        try:
            data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
            empty = True
            for d in data:
                if d != 0:
                    empty = False
            if empty:
                continue
            if debug:
                logger.info(data)
            if data[2] == 0:
                continue
            c = decode(data)
            # print(c)
            if c != '\n':
                result += c
                count += 1
            # print(count)
            if count == 10:
                tagid = result
                print('TagID:' + tagid)
                result = ''
                count = 0
                with open("Database.csv") as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        if row["RFID"] == tagid:
                            RFidRegistered = True
                            print("Welcome " + row["name"])
                            wiringpi.digitalWrite(6, 1)  # Write 1 ( HIGH ) to pin 6
                            push_server(1, )

                            sleep(500 / 1000)  # 500ms
                            wiringpi.digitalWrite(6, 0)  # Write 1 ( HIGH ) to pin 6
                            push_server(0, )

        except usb.core.USBError as e:
            if e.errno == 110:  # 'Operation timed out':
                # print(e)
                print('Please insert RFID card!')
                continue
            logger.error(e)
            continue
    usb.util.release_interface(dev, interface)
    dev.attach_kernel_driver(interface)
    print("scanner reading terminated")


if __name__ == "__main__":
    read_rfid()