# Commands from FruityWifi

class Commands(MenuOption):
    
    def __init__(self):
        # TO BE IMPLEMENTED
        MenuOption.__init__(self)

    def redraw(self, menu):
        lcd.clear()
        menu.write_row(0, "# TO BE IMPLEMENTED")
