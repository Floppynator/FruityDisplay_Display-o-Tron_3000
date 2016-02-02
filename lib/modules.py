# Modules from FruityWifi
import sys
sys.path.append('/')
from dot3k.menu import MenuOption
import dot3k.backlight as backlight
import dot3k.lcd as lcd
from webclient import Webclient
import time
from consoleMessages import ConsoleMessages

class Modules(MenuOption):
    
    def __init__(self):
        self.consoleMessages = ConsoleMessages()
	self.ready = False
	self.modules = []
	self.selected_module = 0	
	self.last_update = 0
	
        MenuOption.__init__(self)

    def setup(self, config):
        MenuOption.setup(self, config)
        
        self.whitelist = self.getWhitelist(config)
        self.blacklist = self.getBlacklist(config)
        self.whitelist_status = self.getWhitelistStatus(config)
        self.blacklist_status = self.getBlacklistStatus(config)

        lcd.create_char(0, [0, 4, 14, 0, 0, 14, 4, 0])  # Up down arrow

        # init webclient
        self.webclient = Webclient(config)
        
        # get the modules as JSON
	complete_modules = self.getModules()
	
        for line in complete_modules:
            if self.whitelist:
                if line in self.whitelist:
                    self.modules.append(line)
            else:
                self.modules.append(line)
          
            if self.blacklist_status:
                if line in self.blacklist and line in self.modules:
                    self.modules.remove(line)

	self.ready = True
        
    def getAnimFrame(self, char, fps):
        return char[int(round(time.time() * fps) % len(char))]
 
    def getModules(self):
        execute = "/module"
    	return self.webclient.submitGet("api=" + str(execute)).json()
    	

    def getWhitelistStatus(self, config):
	white_list_status = config.get("white_list", "status")
	
	if white_list_status == "True" or white_list_status == "true":
	    white_list_status = True
	else:
	    white_list_status = False

	return white_list_status

    def getWhitelist(self, config):
	white_list = config.get("white_list", "modules")
	white_list = white_list.split("|")
	return white_list

    def getBlacklistStatus(self, config):
	black_list_status = config.get("black_list", "status")

	if black_list_status == "True" or black_list_status == "true":
            black_list_status = True
        else:
            black_list_status = False

	return black_list_status

    def getBlacklist(self, config):
	black_list = config.get("black_list", "modules")
        black_list = black_list.split("|")
        return black_list

    def prev_module(self):
	module = self.selected_module - 1
        if module < 0:
            module = len(self.modules) - 1
        return module
	
    def next_module(self):
        module = self.selected_module + 1
        if module >= len(self.modules):
            module = 0
        return module

    def down(self):
        self.selected_module = self.next_module()
        self.ready = True

    def up(self):
	self.selected_module = self.prev_module()
	self.ready = True

    def right(self):
	v_module = self.modules[self.selected_module]

        isRunning = self.getModuleStatus(self.modules[self.selected_module])

        if isRunning == "Y":
            # module is running, stop it
            execute = "/module/" + v_module + "/stop"
            self.consoleMessages.show_info("Stoping module: " + str(v_module) + "")
        else:
            # module is not running, start it
            execute = "/module/" + v_module + "/start"
            self.consoleMessages.show_info("Starting module: " + str(v_module) + "")

        backlight.set_bar(0, 20)
        result = self.webclient.call_api(execute)

        # fire up bargraph leds! Wohoo
        for i in range(100):
            backlight.set_graph(i / 70.0)
            time.sleep(0.005)
            
        # disable leds =(
        backlight.set_graph(0)

        self.ready = True

        try:
            if result[0] == True:
                return "Y"
            else:
                return "N"    
        except:
            return "E"
                                         
    def getModuleStatus(self, v_module):
        self.consoleMessages.show_info("Get module status for: " + str(v_module) + "")
        execute = "/module/" + v_module
        result = self.webclient.call_api(execute)

	if result[0] == True:
            self.consoleMessages.show_info("Status for module " + str(v_module) + " is [Y]")
            return "Y"
        else:
            self.consoleMessages.show_info("Status for module " + str(v_module) + " is [N]")
            return "N"

    def redraw_modules(self, menu):
        if not self.ready:
            menu.clear_row(0)
            menu.write_row(1, 'No modules!')
            menu.clear_row(2)
            return False
	
	if len(self.modules) > 2:
            self.draw_module(menu, 0, self.prev_module())

        self.draw_module(menu, 1, self.selected_module)

        if len(self.modules) > 1:
            self.draw_module(menu, 2, self.next_module())

        self.ready = False

    def draw_module(self, menu, row, index):
	moduleName = self.modules[index]

        icon = ' '
	
	# if selected module 
        if self.selected_module == index:
            if self.getModuleStatus(moduleName) == "Y":
                # module is selected and running then show a stop button
                icon = '[Y]'
            else:
                # module is selected and isnt running show a play button
                icon = chr(0) + '[N]'
      
        menu.write_option(row, moduleName, icon)
        
    def redraw(self, menu):
        
	if self.ready == True:
	    self.redraw_modules(menu)
