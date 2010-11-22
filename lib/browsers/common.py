
#
# Browser Accelerator
# Copyright 2010 Patryk Jaworski <skorpion9312@gmail.com>
# License: GNU GPLv3
#

class browser:
	def configure(self):
		raise TypeError;
	
	def getNames(self):
		raise TypeError;

	def getBrowsersBin(self):
		raise TypeError;

	def getProfileDir(self, name):
		raise TypeError;

	def open(self, path):
		raise TypeError;
	
	def close(self, path):
		raise TypeError;

	def getProfilePath(self):
		raise TypeError;

