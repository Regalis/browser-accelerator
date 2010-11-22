#!/usr/bin/python2

#
# Browser Accelerator
# Copyright 2010 Patryk Jaworski <skorpion9312@gmail.com>
# License: GNU GPLv3
# 

import sys;
import os;

from lib.config import BAConfig;
import lib.GnuPG as GnuPG;

class browserAccelerator:
	__version="1.0";
	__browsers={};
	__browserProfile="%s.ba.tar";

	def __init__(self):
		self.__printHeader();
		if len(sys.argv) < 2:
			self.__printUsage();
			sys.exit(1);
		self.__config=BAConfig();
		if not GnuPG.enabled():
			print "[W] Disabling GnuPG capabilities.";
		
		if sys.argv[1]=="--help":
			self.__printUsage();
			sys.exit(0);
		elif sys.argv[1]=="--configure":
			print "[I] Running an interactive configurator...";
			self.__config.configure();
			sys.exit(0);
		else:
			if not self.__config.load():
				print "[E] Unable to load configuration file. Please run browser-accelerator with --configure option first.";
				sys.exit(1);
			self.__CONFIG=self.__config.getConfig();
			self.__loadBrowsers();
			try:
				module=self.__browsers[sys.argv[1]];
				browser=__import__("lib.browsers.%s" % (module), globals(), locals(), "browser", -1);
				browser=browser.browser();
				profileDir="%s/%s" % (self.__config.getConfigDir(), self.__browserProfile %(sys.argv[1]));
				if GnuPG.enabled() and self.__CONFIG["use_gnupg"]=="True":
					profileDir=profileDir+".gpg";
				if not os.path.exists(profileDir):
					if GnuPG.enabled() and self.__CONFIG["use_gnupg"]!="True":
						if os.path.exists("%s.gpg" % (profileDir)):
							print "[W*] Security warning! Please decrypt or delete your browser package...";
							sys.exit(2);
					print "[I] Preparing browser profile...";
					bp="%s/%s" % (self.__config.getHomeDir(), browser.getProfileDir(sys.argv[1]));
					if not os.path.exists(bp):
						print "[E] Unable to find browser profile, please run %s first..." % (sys.argv[1]);
						sys.exit(1);
					# TODO: Prepare profile...
			except KeyError:
				print "[E] Unsupported browser: %s" % (sys.argv[1]);

	def __loadBrowsers(self):
		modules=os.listdir("lib/browsers");
		for m in modules:
			if m=="__init__.py" or m=="common.py" or m[-4:]==".pyc":
				continue;
			module=__import__("lib.browsers.%s" % (m[0:m.find(".")]), globals(), locals(), "browser", -1);
			browser=module.browser();
			names=browser.getNames();
			for n in names:
				self.__browsers[n]=m[0:m.find(".")];	

	def __printHeader(self):
		print " Browser Accelerator v%s ".center(50,"=") % (self.__version);
		print "= Author: Patryk Jaworski";
		print "= Contact: skorpion9312@gmail.com";
		print "= License: GNU GPLv3";
		print " Copyrigth (c) by Patryk Jaworski".center(50, "=")+"\n";
	
	def __printUsage(self):
		print "\n Usage:";
		print "\t %s [option] OR [browser]" % (sys.argv[0]);
		print "\n Options:";
		print "\t--configure".ljust(20),;
		print "Run an interactive configurator";
		print "\t--help".ljust(20),;
		print "Print this help message";
		print "";

browserAccelerator();
