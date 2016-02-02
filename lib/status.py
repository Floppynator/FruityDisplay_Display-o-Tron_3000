# copied from https://github.com/pimoroni/dot3k/blob/master/python/examples/plugins/graph.py

import psutil
import subprocess
import time
import socket
import fcntl
import struct
from dot3k.menu import MenuOption

def run_cmd(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = p.communicate()[0]
    return output


class IPAddress(MenuOption):
    """
    A plugin which gets the IP address for wlan0
    and eth0 and displays them on the screen.
    """
    def __init__(self):
        self.mode = 0
        self.wlan0 = self.get_addr('wlan0')
        self.eth0 = self.get_addr('eth0')
        self.is_setup = False
        MenuOption.__init__(self)

    def get_addr(self, ifname):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            return socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', ifname[:15].encode('utf-8'))
            )[20:24])
        except IOError:
            return 'Not Found!'

    def redraw(self, menu):
        if not self.is_setup:
            menu.lcd.create_char(0, [0, 4, 14, 0, 0, 14, 4, 0])  # Up down arrow
            self.is_setup = True

        menu.write_row(0, 'IP Address')
        if self.mode == 0:
            menu.write_row(1, chr(0) + ' Wired:')
            menu.write_row(2, self.eth0)
        else:
            menu.write_row(1, chr(0) + ' Wireless:')
            menu.write_row(2, self.wlan0)

    def down(self):
        self.mode = 1

    def up(self):
        self.mode = 0

    def left(self):
        return False

    def cleanup(self):
        self.is_setup = False
