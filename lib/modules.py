# Modules from FruityWifi
from dot3k.menu import MenuOption
import dot3k.lcd as lcd

class Modules(MenuOption):
    
    def __init__(self, modules_out):
	self.ready = False
	self.whitelist = ""
        self.blacklist = ""
        self.whitelist_status = ""
        self.blacklist_status = ""

	self.modules = []
	self.selected_module = 0	
	self.last_update = 0

	for line in modules_out.json():
	    if self.whitelist:
        	if line in self.whitelist:
	            self.modules.append(line)
	    else:
	        self.modules.append(line)
        
	    if self.blacklist_status:
        	if line in self.blacklist and line in modules:
	            self.modules.remove(line)

        MenuOption.__init__(self)

    def setup(self, config):
        self.whitelist = self.getBlacklist(config)
        self.blacklist = self.getWhitelist(config)
        self.whitelist_status = self.getWhitelistStatus(config)
        self.blacklist_status = self.getBlacklistStatus(config)

	run_this_module = [0, 24, 30, 31, 30, 24, 0, 0]
        stop_this_module = [0, 31, 31, 31, 31, 31, 0, 0]
        lcd.create_char(0, run_this_module)
        lcd.create_char(1, stop_this_module)

	self.ready = True

    def getWhitelistStatus(self, config):
	white_list_status = config.get("white_list", "status")
	
	if white_list_status == "True" or white_list_status == "true":
	    white_list_status = True
	else:
	    white_list_status = False

	return white_list_status

    def getWhitelist(self, config):
	white_list = config.get("white_list", "modules")
	self.white_list = white_list.split("|")
	return True

    def getBlacklistStatus(self, config):
	black_list_status = config.get("black_list", "status")

	if black_list_status == "True" or black_list_status == "true":
            black_list_status = True
        else:
            black_list_status = False

	return black_list_status

    def getBlacklist(self, config):
	black_list = config.get("black_list", "modules")
        self.black_list = black_list.split("|")
	return True

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
	# TODO: enable/disable module
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

	icon = ' '
	# TODO: check module status
        if self.selected_module == index:
            icon = chr(0)
      
        menu.write_option(row, moduleName, icon)

    def redraw(self, menu):
	if self.last_update == 0:
	    self.redraw_modules(menu)
