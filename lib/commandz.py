# Commandz from FruityWifi
from dot3k.menu import Menu
from dot3k.menu import MenuOption
import dot3k.lcd as lcd
from configobj import ConfigObj
import time

class Commandz(MenuOption):
    
    def __init__(self):
        # TO BE IMPLEMENTED
	self.config = ConfigObj("init.conf")

	load_array = []
        counter = 0
        load_array.append(["empty",""])

        for item, v in self.config['commands'].iteritems():
            theCommand = v.split("||")
            counter = counter + 1
            load_array.append([theCommand[0].upper(), "screenCommands(str(counter))", theCommand[1], "-"])

	self.load_array = load_array

	# menu struct
	menu = Menu(
	    structure={
		'asdasd':True,
		'ertre':True
	    },
	    lcd=lcd
	)

        MenuOption.__init__(self)

    def right(self):
	# fire command
	return True

    def screenCommands(i):
        # show commands
        display.subItem = True
        itemLF = display.item
        itemUD = display.itemUD
        xpos = 0
        
        lcd.clear()
        lcd.set_cursor_position(0,0)
        lcd.write(prefix + display.menu[itemLF][1][itemUD][0]) # NAME OF COMMAND TO EXEC [position 0 in array]
        
        lcd.set_cursor_position(0,1)
        lcd.write("Execute CMD...")
    
        # execute command
        out = str(execCommand(display.menu[itemLF][1][itemUD][2])) # COMMAND TO EXEC [position 2 in array]
        temp = out
        time.sleep(1)
    
        lcd.set_cursor_position(0,1)
	lcd.message("Done.")
        time.sleep(1)
    
        # Restore Screen
        lcd.clear()
        lcd.set_cursor_position(0,0)
        lcd.write("Commands\n" + str(i) + ". " + display.menu[itemLF][1][itemUD][0])

    def redraw(self, menu):
	#menu.redraw() how can i display a new menu here... hmm
