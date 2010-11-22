
#
# Browser Accelerator
# Copyright 2010 Patryk Jaworski <skorpion9312@gmail.com>
# License: GNU GPLv3
#

import common;
import os;

class browser(common.browser):
	def getBrowserBin(self):
		return ["/usr/bin/chromium", "/usr/bin/google-chrome"];
	
	def getNames(self):
		return ["google-chrome", "chromium"];
	
	def configure(self):
		config=["# Google browsers configuration"];
		binaries=self.getBrowserBin();
		bin_found=False;
		for b in self.getNames():
			bb="/usr/bin/%s" % (b);
			if os.path.exists(bb):
				print " [I] Found %s in %s..." % (b, bb);
				config.append("google_%s_bin=%s" % (b, bb));
				bin_found=True;
		if not bin_found:
			print " [W] Browsers not found...";
		config.append("# End Google browsers configuration");
		return config;

	def getProfileDir(self, name):
		if name not in ("chromium", "google-chrome"):
			raise TypeError("I support only chromium and google-chrome...");
		return ".config/%s" % (name); 

