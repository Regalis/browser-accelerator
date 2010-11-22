#
# Browser Accelerator
# Copyright 2010 Patryk Jaworski <skorpion9312@gmail.com>
# License: GNU GPLv3
# 

def getLine(msg, required=False, default=None):
	while(True):
		answer=raw_input("[G] %s [%s]: " % (msg, default));
		if default is not None and not answer:
			print "[I] Using default value (%s)..." % (default);
			answer=default;
		if not answer and required:
			print "[W] This field is required...";
			continue;
		return answer;
		
def mktar(base, source, target):
	os.chdir(base);
	tar=tarfile.open(target, "w");
	source=source[(source.find(base)+len(base)+1):];
	tar.add(source);
	tar.close();
	
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
