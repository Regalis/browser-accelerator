# 
# Browser Accelerator
# Copyright 2010 Patryk Jaworski <skorpion9312@gmail.com>
# License: GNU GPLv3
#

_USEGNUPG=None;
_GPG=None;

try:
	import GnuPGInterface;
	_USEGNUPG=True;
except ImportError:
	_USEGNUPG=False;

if _USEGNUPG:
	_GPG=GnuPGInterface.GnuPG();

def enabled():
	return _USEGNUPG;

def listSecretKeys():
	list={};
	keys=_GPG.run(["--list-secret-keys"], create_fhs=['stdin', 'stdout']);
	keylist=keys.handles['stdout'].read();
	keys.handles['stdout'].close();
	if len(keylist) < 1:
		return {};
	KID=None;
	keylist=keylist.split("\n");
	for line in keylist:
		type=line[0:3];
		if type not in ('sec', 'uid'):
			continue;
		if type=='sec':
			KID=line[line.find("/")+1:line.rfind(" ")].strip();
		if type=='uid':
			list[KID]=line[3:].strip();
	return list;
