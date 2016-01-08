# Modules from FruityWifi
from dot3k.menu import MenuOption
import dot3k.lcd as lcd

class Modules(MenuOption):
    
    def __init__(self):
        # TO BE IMPLEMENTED
        MenuOption.__init__(self)

    def redraw(self, menu):
        lcd.clear()
        menu.write_row(0, "TO BE IMPLEMENTED :(")
