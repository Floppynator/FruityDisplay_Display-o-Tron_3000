# Display the About Page from FruityDisplay

# includes
import dot3k.lcd as lcd
from dot3k.menu import MenuOption

class About(MenuOption):
    def __init__(self):
        MenuOption.__init__(self)

    def redraw(self, menu):
        lcd.clear()
	menu.write_option(row=0, text="About this App")
        menu.write_option(row=1, text="Site: https://github.com/Floppynator/FruityDisplay_DisplayOTron3000", scroll=True)
	lcd.set_cursor_position(0,2)	
	lcd.write("Twitter: @HA1pe")
    
    
class AboutFruityWifi(MenuOption):
    
    def __init__(self, FruityWifi, Firmware):
        self.fruityWifiVersion = "FruityWiFi v" + FruityWifi
        self.fruityFirmware = "Firmware v"+ Firmware
        
        MenuOption.__init__(self)

    def redraw(self, menu):
        lcd.clear()
        menu.write_option(row=0, text="About FruityWifi | Site: http://www.fruitywifi.com | Twitter: @fruitywifi @xtr4nge", scroll=True)
        menu.write_option(row=1, text=self.fruityWifiVersion, scroll=True)
        menu.write_option(row=2, text=self.fruityFirmware, scroll=True)
