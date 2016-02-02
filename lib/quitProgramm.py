# Handle the quit process for this programm

# includes
import dot3k.lcd as lcd
from dot3k.menu import MenuOption
import dot3k.backlight as backlight
import time
import sys

class QuitProgramm(MenuOption):
    def __init__(self):
        MenuOption.__init__(self)

    def redraw(self, menu):
        print "Bye ;)"
	lcd.clear()
	lcd.set_cursor_position(4,1)
	lcd.write("Bye Bye!")
	time.sleep(2)
	lcd.clear()
	backlight.rgb(0,0,0)
	sys.exit()
        
