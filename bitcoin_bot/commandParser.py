import os,time,re
import subprocess as sp
import difflib
#from difflib_data import *

FILE="/opt/scripts/bitcoin_bot/command.list"

class CommandParser(object):

#	def __init__(self):
#		a=self

	def getCommand(self,command):
		print "cmd: "+command+"-"
		try:
			command=str(command).lower()
			file = open(FILE,"r+")
			cmd = file.readlines()
			
			i=0
			for c in cmd:
				c=c.rstrip('\n')
				if c.startswith(command.split(' ')[0]):
					return str(c.split(":")[1])
				i=+1
			file.close()
			x=str(CommandParser().getCloserCommand(command.split(' ')[0])[0])
			print "Proximo: "+x
			return CommandParser().getCommand(x)#+' '+str(command.split(' ')[:1])
		except Exception as e:
			return False

	
	def getCloserCommand(self,command):
		return difflib.get_close_matches(command,CommandParser().getList().split(','))

	def getList(self):
		file = open(FILE,"r+")
	        cmd = file.readlines()
		lst=""
		for c in cmd:
			c=c.rstrip('\n')
			lst+=","+str(c.split(':')[0])
		return	re.sub("^,","",lst)
	
	def runAndReturn(self,command):
		ret=str(sp.check_output([command],shell=True)[:-1])
		return ret
	
	
	
	
#	print "Comando: "+getCommand("carga")
#	print getList()
#	print runAndReturn(getCommand("ip"))
