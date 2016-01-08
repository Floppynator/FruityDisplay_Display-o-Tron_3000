#!/usr/bin/env python
import sys
sys.path.append('lib')

# FruityDisplay for Display O Tron 3000
from dot3k.menu import Menu
import dot3k.backlight as backlight
import dot3k.lcd as lcd
import dot3k.joystick
import time
import configobj as config

# libs
from about import AboutFruityWifi, About
from status import IPAddress, GraphTemp, GraphCPU, GraphNetSpeed
from settings import Backlight, Randomlight, Contrast
from modules import Modules
from commandz import Commandz

# versions
__FIRMWARE__ = "1.0-o-tron"
__FRUITYWIFI__ = "2.2"

# fire up the display background with the color from config file
backlight.rgb(255,255,255)

# menu struct
menu = Menu(
    structure={
        'Modules': Modules(),
        'Commands': Commandz(),
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
            'Contrast': Contrast(lcd),
            'Randomlight': Randomlight(backlight)            
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

@dot3k.joystick.on(dot3k.joystick.LEFT)
def handle_left(pin):
    menu.left()

@dot3k.joystick.on(dot3k.joystick.RIGHT)
def handle_right(pin):
    menu.right()

def exit():
	print "Bye ;)"
	lcd.clear()
	lcd.set_cursor_position(4,1)
	lcd.write("Bye Bye!")
	time.sleep(2)
	lcd.clear()
	backlight.rgb(0,0,0)
	sys.exit()


while 1:
	try:	
	    menu.redraw()
            time.sleep(0.01)
	except KeyboardInterrupt:
	    print 
	    exit()

