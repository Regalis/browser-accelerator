
#
# Browser Accelerator
# Copyright 2010 Patryk Jaworski <skorpion9312@gmail.com>
# License: GNU GPLv3
#

import common;
import os;

class browser(common.browser):
	def getBrowserBin(self):
		return ["/usr/bin/opera", "/usr/local/bin/opera"];
	
	def getNames(self):
		return ["opera"];
	
	def configure(self):
		config=["# Opera configuration"];
		binaries=self.getBrowserBin();
		bin_found=False;
		for b in binaries:
			if os.path.exists(b):
				print " [I] Found Opera in %s..." % (b);
				config.append("opera_bin=%s" % (b));
				bin_found=True;
				break;
		if not bin_found:
			print " [W] Browser Opera not found...";
		config.append("# End Opera configuration");
		return config;
