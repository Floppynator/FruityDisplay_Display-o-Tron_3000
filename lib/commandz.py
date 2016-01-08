# Commandz from FruityWifi
from dot3k.menu import Menu
from dot3k.menu import MenuOption
import dot3k.lcd as lcd
from configobj import ConfigObj
import time

class Commandz(MenuOption):
    
    def __init__(self):
	self.ready = False
	self.config = ConfigObj("init.conf")
	self.cmds = None
	self.selected_cmd = 0
	self.last_update = 0
	
	MenuOption.__init__(self)	

    def setup(self, config):
	MenuOption.setup(self, config)
	
	if 'commands' in self.config.sections():
            self.cmds = self.config.options('commands')
            self.ready = True

    def prev_cmd(self):
	cmd = self.selected_cmd - 1
        if cmd < 0:
            cmd = len(self.cmds) - 1
        return cmd
	
    def next_cmd(self):
        cmd = self.selected_cmd + 1
        if cmd >= len(self.cmds):
            cmd = 0
        return cmd
    
    def down(self):
        self.selected_cmd = self.next_cmd()

    def up(self):
	self.selected_cmd = self.prev_cmd()

    def right(self):
	# fire cmd
	self.last_update = 1

	lcd.clear()
	lcd.write("Execute CMD")
	lcd.set_cursor_position(0,1)
	cmd = self.config.get('commands', self.cmds[self.selected_cmd])
	cmd = cmd.split(",")
	lcd.write(cmd[0])
	time.sleep(2)
	lcd.clear()
	lcd.set_cursor_position(6,1)
	lcd.write("Done.")
	time.sleep(1)

	self.last_update = 0	
	
	# TODO EXECUTE THIS COMMAND	
	return True

    def redraw_commands(self, menu):
        if not self.ready:
            menu.clear_row(0)
            menu.write_row(1, 'No commands!')
            menu.clear_row(2)
            return False

        if len(self.cmds) > 2:
            self.draw_cmd(menu, 0, self.prev_cmd())

        self.draw_cmd(menu, 1, self.selected_cmd)

        if len(self.cmds) > 1:
            self.draw_cmd(menu, 2, self.next_cmd())

    def draw_cmd(self, menu, row, index):
	cmd = self.config.get('commands', self.cmds[index])
        title = cmd.split(',')[0]
        exec_command = cmd.split(',')[1]

	icon = ' '
        if self.selected_cmd == index:
            icon = chr(252)

        menu.write_option(row, title, icon)

    def redraw(self, menu):
	if self.last_update == 0:
 	    self.redraw_commands(menu)
