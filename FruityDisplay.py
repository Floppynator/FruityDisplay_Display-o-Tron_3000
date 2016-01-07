#!/usr/bin/env python
import sys
sys.path.append('lib')

# FruityDisplay for Display O Tron 3000
from dot3k.menu import Menu
import dot3k.backlight as backlight
import dot3k.lcd as lcd
import dot3k.joystick
import time
from configobj import ConfigObj

# libs
from about import AboutFruityWifi, About
from status import IPAddress, GraphTemp, GraphCPU, GraphNetSpeed
from settings import Backlight, Randomlight, Contrast
from modules import Modules
#from commands import Commands

config = ConfigObj("init.conf")

# versions
__FIRMWARE__ = "1.0-o-tron"
__FRUITYWIFI__ = "2.2"

# fire up the display background with the color from config file
backlight.rgb(int(config["lcd"]["default_color"][0]), int(config["lcd"]["default_color"][1]), int(config["lcd"]["default_color"][2]) )

# menu struct
menu = Menu(
    structure={
        'Modules': Modules(),
 #       'Commands': Commands(),
        'About': {
            'This App': About(),
            'FruityWifi': AboutFruityWifi(__FRUITYWIFI__, __FIRMWARE__)
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
    lcd.set_cursor_position(0,0)
    lcd.write("Welcome!")
    lcd.set_cursor_position(0,1)
    lcd.write("FruityWiFi " +  __FRUITYWIFI__)
    time.sleep(2)

def loadingScreen():
    lcd.clear()
    
    # set brigthness 
    backlight.set_bar(0, 20)
    
    # write loading message to lcd
    lcd.set_cursor_position(3,1)
    lcd.write("Loading...")
    
    # fire up bargraph leds! Wohoo
    for i in range(100):
        backlight.set_graph(i / 70.0)
        time.sleep(0.005)
        
    # disable leds =(
    backlight.set_graph(0)


# Show loading screen
loadingScreen()
# show welcome message
showWelcomeMessage()

@dot3k.joystick.on(dot3k.joystick.UP)
def handle_up(pin):
    menu.up()


@dot3k.joystick.on(dot3k.joystick.DOWN)
def handle_down(pin):
    menu.down()

@dot3k.joystick.on(dot3k.joystick.RIGHT)
def handle_right(pin):
    menu.right()

while 1:
    menu.redraw()
    time.sleep(0.01)
