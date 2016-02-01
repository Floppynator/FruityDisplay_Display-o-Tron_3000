# Modules from FruityWifi
import sys
sys.path.append('/')
from dot3k.menu import MenuOption
import dot3k.lcd as lcd
from webclient import Webclient
import time

class Modules(MenuOption):
    
    def __init__(self):
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
        
	run_this_module = [0, 24, 30, 31, 30, 24, 0, 0]
        stop_this_module = [0, 31, 31, 31, 31, 31, 0, 0]
        # Add a Pirat! Harr Harr Harr
        module_is_running = [[0x00, 0x1f, 0x0b, 0x03, 0x00, 0x04, 0x11, 0x1f],[0x00, 0x1f, 0x16, 0x06, 0x00, 0x08, 0x03, 0x1e],[0x00, 0x1f, 0x0b, 0x03, 0x00, 0x04, 0x11, 0x1f],[0x00, 0x1f, 0x05, 0x01, 0x00, 0x02, 0x08, 0x07]]
        lcd.create_char(0, run_this_module)
        lcd.create_char(1, stop_this_module)
        lcd.create_char(3, self.getAnimFrame(module_is_running, 2))

        # init webclient
        self.webclient = Webclient(config.get("api","server"), config.get("api","token"))
        
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

    def up(self):
	self.selected_module = self.prev_module()

    def right(self):
	# TODO: enable/disable module over webclient
	return True

    def getModuleStatus(self):
    	# TODO: read menu status from weblcient
    	return True

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

    def draw_module(self, menu, row, index):
	moduleName = self.modules[index]
 
 	# show the Pirat for running module!
	if self.getModuleStatus():
	    icon = chr(2)
	else:
	    icon = ' '
	
	# if selected module 
        if self.selected_module == index:
            if self.getModuleStatus():
                # module is selected and running then show a stop button
                icon = chr(1)
            else:
                # module is selected and isnt running show a play button
                icon = chr(0)
      
        menu.write_option(row, moduleName, icon)

    def redraw(self, menu):
        
	if self.last_update == 0:
	    self.redraw_modules(menu)
