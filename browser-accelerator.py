#!/usr/bin/python2
# coding=utf-8

# 
# Copyright 2010 Patryk Jaworski <skorpion9312@gmail.com>
# Licence: GNU GPLv3
# 

GNUPG=True;
GNUPG_MODULE=True;

import sys;
import tarfile;
import commands;
import os;
import getpass;
import shutil;
try:
	import gnupg;
except ImportError, e:
	GNUPG_MODULE=False;
	GNUPG=False;		

class browserAccelerator:
	__supportedBrowsers={"chromium": ("--user-data-dir=%s", ".config/chromium"), "chromium-browser": ("--user-data-dir=%s", ".config/chromium"), "opera": ("-pd %s", ".opera")};
	__browsers={};
	__homeDir=None;
	__configDir=None;
	__gpg=None;
	__config=None;
	__user=None;
	
	def __init__(self, GNUPG, GNUPG_MODULE):
		self.__GNUPG=GNUPG;
		self.__GNUPG_MODULE=GNUPG_MODULE;
		self.printHeader();
		self.__homeDir=os.getenv("HOME");
		self.__user=os.getenv("USER");
		if not self.__homeDir or not self.__user:
			print "[E] Unable to read required environment variables: HOME or UID...";
			print self.__homeDir+" "+self.__user;
			sys.exit(1);
		self.__configDir="%s/%s" % (self.__homeDir, ".browser-accelerator");
		if len(sys.argv) < 2:
			self.__printUsage();
			sys.exit(1);
		if sys.argv[1] == "--configure":
			self.__configure();
			sys.exit(0);
		if sys.argv[1] == "--help":
			self.__printUsage();
			sys.exit(0);
		self.__readConfig();
		try:
			if self.__config["use_gnupg"]=="True":
				print "[I] Initializing GnuPG...";
				self.__initGPG();
		except:
				pass;
		if sys.argv[1] not in self.__supportedBrowsers:
			print "[E] Unsupported browser: %s" % (sys.argv[1]);
			self.__printUsage();
			sys.exit(1);
		if not os.path.exists("%s/.gnupg" % (self.__homeDir)):
			print "[W] Unable to find .gnupg directory. Please configure your GnuPG first...";
			self.__GNUPG=False;			
		if not self.__GNUPG_MODULE:
			print "[W] Unable to load optional module *gnupg*...";
		if not self.__GNUPG:	
			print "[I] Disabling encryption capabilities...";
		self.__run(sys.argv[1]);
	
	def __readConfig(self):
		if not os.path.exists(self.__configDir) or not os.path.exists(self.__configDir+"/config"):
			print "[I] Running configurator...";
			self.__configure();
		conf=open("%s/config" % (self.__configDir), "r");
		lines=conf.readlines();
		if len(lines) < 2:
			print "[E] Error in configuration file, please check it...";
			sys.exit(1);
		self.__config={};
		for l in lines:
			e=l.find("=");
			if e < 1:
				print "[E] Error in configuration file, please check it...";
				sys.exit(1);
			name=l[0:e].strip();
			value=l[(e+1):].strip();
			self.__config[name]=value;	
			
	def __initGPG(self):
		self.__gpg=gnupg.GPG(gnupghome="%s/.gnupg" % (self.__homeDir));
			
	def __configure(self):
		print "[I] Searching for installed browsers...";
		binDirs=("/usr/bin/","/usr/local/bin/");
		for browser in self.__supportedBrowsers:
			for dir in binDirs:
				bin="%s%s" % (dir, browser);
				if os.path.exists(bin):
					print "[I] Found %s in %s..." % (browser, bin);
					self.__browsers[browser]=bin;
		usegpg=False;
		if self.__GNUPG:
			usegpg=utils.getLine("Do you want to use GnuGP to encrypt/decrypt your browser profiles (yes/no)?", True, "no").lower();
			if usegpg in ("no","n"):
				usegpg=False;
			else:
				usegpg=True;
		if usegpg:
			self.__initGPG();
			keys=self.__gpg.list_keys(True);
			if len(keys) < 1:
				print "[E] Unable to find any secret keys... Please configure your GnuPG first.";
				sys.exit(1);
			i=1;
			print "[I] Select key which will be use to encrypt/decrypt...";
			print "[I] Secret keys list:";
			for key in keys:
				print "[%d] %s (%s)" % (i, key["keyid"], key["uids"][1]);
				i=i+1;
			while(True):
				key=utils.getLine("Enter key index (eg. 1)", True, "1");
				try:
					if int(key) not in range(1, i):
						continue;
					else:
						break;
				except ValueError:
					continue;
		if not os.path.exists(self.__configDir):
			print "[I] Creating configuration directory (%s)..." % (self.__configDir);
			try:
				os.mkdir(self.__configDir);
			except OSError, e:
				print "[E] Error while creating directory: %s" % (e);
				sys.exit(1);
		if usegpg:
			use_gnupg="True";
			gnupg_key=keys[(int(key)-1)]["keyid"];
		else:
			use_gnupg="False";
			gnupg_key="None";
		config=open("%s/config" % (self.__configDir), "w");
		config.write("use_gnupg=%s\n" % (use_gnupg));
		config.write("gnupg_key=%s\n" % (gnupg_key));
		for browser in self.__browsers:
			config.write("%s=%s\n" % (browser, self.__browsers[browser]));
		config.close();
		print "[I] Configuration saved...";
	
	def __run(self, browser):
		print "[I] Checking %s" % (browser);
		bin=None;
		try:
			bin=self.__config[browser];
		except KeyError:
			print "[E] Please add %s to your configuration file or try to run browser-accelerator with --configure option..." % (browser);
			sys.exit(1);
		end=bin.find(" ");
		if end < 0:
			end=len(bin);
		if not os.path.exists(bin[0:end]):
			print "[E] Unable to find your browser in %s..." % (browser);
			sys.exit(1);
		use_gnupg=False;
		try:
			if self.__config["use_gnupg"]=="True":
				use_gnupg=True;
				try:
					key=self.__config["gnupg_key"];
					if not key:
						raise KeyError;
				except KeyError:
					print "[E] Please specify \"gnupg_key\" in your configuration file...";
					os.remove(tmp);
					sys.exit(1);
		except KeyError:
			pass;
		profile="%s/%s" % (self.__homeDir, self.__supportedBrowsers[browser][1]);
		if not os.path.exists(profile):
			print "[E] Unable to find your browser profile in %s. Please run %s first..." % (profile, bin);
			sys.exit(1);
		localProfile="%s/%s.tar.bz2" % (self.__configDir, browser);
		if use_gnupg:
			if os.path.exists(localProfile):
				print "[I] Detected old package in profile directory...";
				print "[I] Using GnuPG to encrypt tarball...";
				self.__gpg.encrypt_file(open(localProfile,"r"), key, output="%s.gpg" % (localProfile));
				os.remove(localProfile);
				print "[I] Done...";
			localProfile=localProfile+".gpg";
		tmp="/dev/shm/%s-%s" % (self.__user, localProfile[(localProfile.rfind("/")+1):]);
		if not os.path.exists(localProfile):
			if not use_gnupg:
				if os.path.exists(localProfile+".gpg"):
					print "[SW] Security warning!";
					print "[SW] Detected encrypted profile tarball. Please run browser-accelerator with GnuPG enabled (edit your configuration file), manually decrypt your tarball *or* remove it to continue without encryption.";
					sys.exit(1);
			if use_gnupg:
				tmp=tmp[0:-4];
			print "[I] Creating profile tarball...";
			base="%s" % (profile[0:profile.rfind("/")]);
			utils.mktar(base, profile, tmp);
			print "[I] Done...";
			if use_gnupg:
				print "[I] Using GnuPG to encrypt tarball..."; 
				self.__gpg.encrypt_file(open(tmp,"r"), key, output=tmp+".gpg");
				print "[I] Done...";
				os.remove(tmp);
				tmp=tmp+".gpg";
			print "[I] Moving tarball to profile directory...";
			shutil.move(tmp, localProfile);
			print "[I] OK...";
		print "[I] Preparing profile...";
		RAMProfile="/dev/shm/%s-%s" % (self.__user, browser);
		tarball=localProfile;
		if use_gnupg:
			password=getpass.getpass("[G] Enter your GnuPG password: ");
			print "[I] Decrypting browser data...";
			self.__gpg.decrypt_file(open(localProfile, "r"), output=tmp[0:-4], passphrase=password);
			# TODO:
			# I don't know how to catch exception (ValueError - eg. bad password) reported by gnupg thread :(
			if not os.path.exists(tmp[0:-4]):
				print "[E] Decrypting error...";
				sys.exit(1);
			tarball=tmp[0:-4];	
		print "[I] Unpacking tarball...";
		utils.extar(RAMProfile, tarball);
		os.remove(tarball);
		print "[I] Done...";
		RAMProfile="%s/%s" % (RAMProfile, self.__supportedBrowsers[browser][1][self.__supportedBrowsers[browser][1].rfind("/")+1:]);
		cmd="%s %s" % (self.__config[browser], self.__supportedBrowsers[browser][0] % (RAMProfile));
		print "[I] Executing %s" % (cmd);
		try:
			status = commands.getstatusoutput(cmd);
		except KeyboardInterrupt:
			print "[I] Exiting...";
		print "[I] Done...";
		browserbase=self.__supportedBrowsers[browser][1][self.__supportedBrowsers[browser][1].rfind("/")+1:];
		tmpbase=RAMProfile[0:RAMProfile.find("/"+browserbase)];
		print "[I] Creating tarball...";
		utils.mktar(tmpbase, "%s/%s" % (tmpbase, browserbase), tarball);
		shutil.rmtree(tmpbase);
		if use_gnupg:
			print "[I] Encrypting tarball...";
			self.__gpg.encrypt_file(open(tarball,"r"), key, output=localProfile);
			os.remove(tarball);
		else:
			shutil.move(tarball, localProfile);
		print "\n"+" Done ".center(50, "=")+"\n";
			
	def __printUsage(self):
		print "Usage:";
		print "\t%s [option] OR [browser]" % (sys.argv[0]);
		print "\nOptions:";
		print "\t--configure".ljust(20, " "),;
		print "Run an interactive configurator";
		print "\t--help".ljust(20, " "),;
		print "Print this help message";
		print "\nBrowsers:";
		for browser in self.__supportedBrowsers:
			print "-> %s" % (browser);
		print "";
	
	def printHeader(self):
		print " Browser Accelerator ".center(50,"=");
		print "= Author: Patryk Jaworski";
		print "= Contact: skorpion9312@gmail.com";
		print "= Licence: GNU GPLv3";
		print " Copyright (c) by Patryk Jaworski ".center(50,"=")+"\n";

class utils:
	@staticmethod
	def getLine(msg, required=False, default=None):
		while(True):
			answer=raw_input("[G] %s [%s]: " % (msg, default));
			if default is not None and not answer:
				print "[I] Setting default value (%s)..." % (default);
				answer=default;
			if not answer and required:
				print "[W] This field is required...";
				continue;
			return answer;
			
	@staticmethod
	def mktar(base, source, target):
		os.chdir(base);
		tar=tarfile.open(target, "w");
		source=source[(source.find(base)+len(base)+1):];
		tar.add(source);
		tar.close();
		
	@staticmethod
	def extar(base, source):
		if not os.path.exists(base):
			try:
				os.mkdir(base);
			except:
				print "[E] Error while creating folder...";
				sys.exit(1);
		os.chdir(base);
		tar=tarfile.open(source, "r");
		tar.extractall();
		tar.close();
		
if __name__=="__main__":
	browserAccelerator(GNUPG, GNUPG_MODULE);

