#!/usr/bin/env python
# -*- coding: UTF-8 -*- 
#
# Copyright (c) 2016 totymedli
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Made with the help of:
# https://wiki.ubuntu.com/DesktopExperienceTeam/ApplicationIndicators#Python_version
# http://candidtim.github.io/appindicator/2014/09/13/ubuntu-appindicator-step-by-step.html

from gi.repository import Gtk
from gi.repository import AppIndicator3 as Appindicator
import signal as Signal
import os as Os
import json as Json

class Indicator:

	def __init__(self, os, gtk, json, appindicator):
		self.path = os.path
		self.execute = os.system
		self.gtk = gtk
		self.json = json
		self.indicator = appindicator.Indicator.new(
			'Dev Launcher',
			self.get_icon_path('offline'),
			appindicator.IndicatorCategory.APPLICATION_STATUS)
		self.indicator.set_status (appindicator.IndicatorStatus.ACTIVE)

		with open(self.get_path('data/commands.json')) as data_file:
			self.commands = json.load(data_file)

		self.indicator.set_menu(self.build_menu())
		self.gtk.main()

	def get_path(self, string):
		return self.path.join(self.path.dirname(self.path.abspath(__file__)), string)

	def get_icon_path(self, icon_name):
		return  self.get_path("icons/%s.svg" % (icon_name))

	def build_menu(self):
		menu = self.gtk.Menu()

		self.item_start = self.gtk.MenuItem('Start')
		self.item_start.connect('activate', self.start_dev)
		menu.append(self.item_start)

		self.item_stop = self.gtk.MenuItem('Stop')
		self.item_stop.connect('activate', self.stop_dev)
		menu.append(self.item_stop)

		for other_item_data in self.commands['other']:
			item_other = self.gtk.MenuItem(other_item_data['label'])
			item_other.connect('activate', self.start_other, other_item_data['commands'])
			menu.append(item_other)
			item_other.show()

		item_quit = self.gtk.MenuItem('Quit')
		item_quit.connect('activate', self.quit)
		menu.append(item_quit)

		self.item_start.show()
		item_quit.show()
		return menu

	def execute_commands(self, commands):
		for command in commands:
			self.execute(command)

	def start_dev(self, source):
		self.execute_commands(self.commands['start'])
		self.item_start.hide()
		self.item_stop.show()
		self.indicator.set_icon(self.get_icon_path('online'))

	def stop_dev(self, source):
		self.execute_commands(self.commands['stop'])
		self.item_stop.hide()
		self.item_start.show()
		self.indicator.set_icon(self.get_icon_path('offline'))

	def start_other(self, source, commands):
		self.execute_commands(commands)

	def quit(self, source):
		self.gtk.main_quit()

if __name__ == "__main__":
	Signal.signal(Signal.SIGINT, Signal.SIG_DFL) # Support for Ctrl + C
	indicator = Indicator(Os, Gtk, Json, Appindicator)
