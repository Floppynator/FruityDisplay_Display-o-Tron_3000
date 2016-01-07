# Display the About Page from FruityDisplay

# includes
import dot3k.lcd as lcd
import dot3k.menu 

class About(MenuOption):
    def __init__(self):     
        MenuOption.__init__(self)

    def left(self):
                return False
    
    def right(self):
                return False
    
    def up(self):
                return False
        
    def down(self):
                return False
        
    def redraw(self, menu):
        lcd.clear()
        menu.write_option(row=0, text="About this App | Site: https://github.com/Floppynator/FruityDisplay_DisplayOTron3000 | Twitter: @HA1pe", scroll=true)
    
    
class AboutFruityWifi(MenuOption):
    
    def __init__(self):
        self.fruityWifiVersion = "FruityWiFi v" + __FRUITYWIFI__
        self.fruityFirmware = "Firmware v"+ __FIRMWARE__
        
        MenuOption.__init__(self)

    def left(self):
                return False
    
    def right(self):
                return False
    
    def up(self):
                return False
        
    def down(self):
                return False
        
    def redraw(self, menu):
        lcd.clear()
        menu.write_option(row=0, text="About FruityWifi | Site: http://www.fruitywifi.com | Twitter: @fruitywifi @xtr4nge", scroll=true)
        menu.write_option(row=1, text=self.fruityWifiVersion, scroll=true)
        menu.write_option(row=2, text=self.fruityFirmware, scroll=true)
