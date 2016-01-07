#!/usr/bin/env python

# FruityDisplay for Display O Tron 3000
from dot3k.menu import Menu
import dot3k.backlight as backlight
import dot3k.lcd as lcd
import time
from configobj import ConfigObj

# libs
from lib.about import AboutFruityWifi, About
from lib.status import IPAddress, GraphTemp, GraphCPU, GraphNetSpeed
from lib.settings import Backlight, Randomlight, Contrast
from lib.modules import Modules
from lib.commands import Commands

config = ConfigObj("init.conf")

# versions
__FIRMWARE__ = "1.0-o-tron"
__FRUITYWIFI__ = "2.2"

# fire up the display background with the color from config file
backlight.rgb(config["lcd"]["default_color"])

# menu struct
menu = Menu(
    structure={
        'Modules': Modules(),
        'Commands': Commands(),
        'About': {
            'This App': About(),
            'FruityWifi': AboutFruityWifi()
        },
        'Status': {
            'IP': IPAddress(),
            'CPU': GraphCPU(backlight),
            'Temp': GraphTemp(backlight)
        }, 
        'Settings': {
            'Display': {
                'Contrast': Contrast(lcd),
                'Backlight': Backlight(backlight),
                'Randomlight': Randomlight (backlight)
            }
        }
    },
    lcd=lcd
)

def showWelcomeMessage():
    lcd.clear()
    lcd.set_cursor_position(3,0)
    lcd.write("Welcome!")
    lcd.set_cursor_position(3,1)
    lcd.write("FruityWiFi " +  __FRUITYWIFI__)
    time.sleep(2)

def loadingScreen():
    lcd.clear()
    
    # set brigthness 
    backlight.set_bar(0, 20)
    
    # write loading message to lcd
    lcd.set_cursor_position(0,0)
    lcd.write("Loading, please wait")
    
    # fire up bargraph leds! Wohoo
    for i in range(50):
        backlight.set_graph(i / 100.0)
        time.sleep(0.05)
        
    # disable leds =(
    backlight.set_graph(0)


# Show loading screen
loadingScreen()
# show welcome message
showWelcomeMessage()

while 1:
    menu.redraw()
    time.sleep(0.01)
