#
# Browser Accelerator
# Copyright 2010 Patryk Jaworski <skorpion9312@gmail.com>
# License: GNU GPLv3
# 

import os;
import sys;
import GnuPG;
import utils;

class BAConfig:
	__homeDir=None;
	__user=None;
	__configDir=None;
	__config=None;
	__configDefault={'use_gnupg': 'False', 'gnupg_key': 'None'};
	
	def __init__(self):
		self.__homeDir=os.getenv("HOME");
		self.__user=os.getenv("USER");
		if not self.__homeDir or not self.__user:
			raise RuntimeError("Unable to get user informations...");
		self.__configDir="%s/.browser-accelerator" % (self.__homeDir);
	
	def getConfigDir(self):
		return self.__configDir;

	def getConfig(self):
		return self.__config;

	def getHomeDir(self):
		return self.__homeDir;

	def getUserName(self):
		return self.__user;

	def configure(self):
		if not os.path.exists("lib/browsers"):
			print "[E] Error - directory lib/browsers not found...";
			sys.exit(1);
		self.__config=[];
		browsers=os.listdir("lib/browsers");
		for b in browsers:
			if b=="__init__.py" or b=="common.py" or b[-4:]==".pyc":
				continue;
			B=__import__("%s.%s" % ("browsers", b[0:b.find(".")]), globals(), locals(), "browser", -1);
			print "[I] Running %s configurator..." % (b[0:b.find(".")]);
			browser=B.browser();
			config=browser.configure();
			self.__config=self.__config+config;
		if GnuPG.enabled():
			try:
				while True:
					answer=utils.getLine('Do you want to use GnuPG? (yes/no)', True, 'yes').lower();
					if answer in ('n', 'no'):
						raise ValueError;
					elif answer in ('y', 'yes'):
						self.__config.append("# GnuPG configuration");
						self.__config.append("use_gnupg=True");
						keys=GnuPG.listSecretKeys();
						if len(keys) < 1:
							print "[E] Unable to find any secret keys... Please configure your GPG first...";
							sys.exit(1);
						while True:
							i=1;
							print "[I] Secret keys list:";
							keyList={};
							for key in keys:
								keyList[i]=key;
								print " %d. %s (%s)" % (i, key, keys[key]);
								i=i+1;
							answer=utils.getLine('Select key index', True, '1');
							try:
								answer=int(answer);
								if answer not in range(1,i):
									continue;
								else:
									self.__config.append("gnupg_key=%s" % (keyList[answer]));
									break;
							except ValueError:
								continue;
						self.__config.append("# End GnuPG configuration");
						break;
					else:
						continue;
			except:
				pass;
		print "[I] Done... Writing configration...";
		if not os.path.exists(self.__configDir):
			print "[I] Creating directory in %s..." % (self.__configDir);
			try:
				os.mkdir(self.__configDir, 0700);
			except OSError:
				print "[E] Error while creating directory...";
				sys.exit(1);
		config=open("%s/config" % (self.__configDir), "w");
		for cfg in self.__config:
			config.write(cfg+"\n");
		config.close();
		print "[I] Configuration saved...";
	
	def load(self):
		if not os.path.exists(self.__configDir) or not os.path.exists(self.__configDir+"/config"):
			return False;
		conf=open("%s/config" % (self.__configDir), "r");
		lines=conf.readlines();
		if len(lines) < 2:
			print "[E] Error in configuration file, please check it...";
			return False;
		self.__config={};
		for l in lines:
			l=l.strip();
			if l[0:1] == "#":
				continue;
			e=l.find("=");
			if e < 1:
				print "[E] Error in configuration file, please check it...";
				sys.exit(1);
			name=l[0:e].strip();
			value=l[(e+1):].strip();
			self.__config[name]=value;
		for key in self.__configDefault:
			try:
				if not self.__config[key]:
					pass;
			except KeyError:
				self.__config[key]=self.__configDefault[key];
		return True;
	
