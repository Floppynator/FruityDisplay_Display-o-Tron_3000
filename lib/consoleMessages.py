#!/usr/bin/env python

class ConsoleMessages():

    def __init__(self):
        self.PURPLE = '\033[95m'
        self.CYAN = '\033[96m'
        self.DARKCYAN = '\033[36m'
        self.BLUE = '\033[94m'
        self.GREEN = '\033[92m'
        self.YELLOW = '\033[93m'
        self.RED = '\033[91m'
        self.BOLD = '\033[1m'
        self.UNDERL = '\033[4m'
        self.ENDC = '\033[0m'
        
    def show_error(self, message):
        print self.RED + self.BOLD + "[-] " + self.ENDC + str(message)

    def show_alert(self, message):
        print self.YELLOW + self.BOLD + "[!] " + self.ENDC + str(message)

    def show_msg(self, message):
        print self.GREEN + self.BOLD + "[+] " + self.ENDC + str(message)

    def show_info(self, message):
        print self.BLUE + self.BOLD + "[*] " + self.ENDC + str(message)
