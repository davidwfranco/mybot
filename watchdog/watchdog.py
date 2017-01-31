#!/usr/bin/python2
import sys
import time
import telepot
from commandParser import CommandParser
from md5	import MD5
from netUtil	import netUtil
cmd = CommandParser()
#Watchdogbot
IMG="/tmp/lastimg.jpg"
def handle(msg):
	
    txt = str(msg['text']).lower().replace(';',' ')
    print str(msg)
		
    if txt.startswith("snap"):
		cmd.runAndReturn(cmd.getCommand(txt.split(' ')[0]))
		sendImage()
		return

    elif cmd.getCommand(txt):
        print "Nao conheco a palavra "+str(cmd.getCommand(txt))+" envie ajuda para conhecer os comando possiveis"
        if len(txt.split(' ')) > 1:
                bot.sendMessage(msg['from']['id'],cmd.runAndReturn(cmd.getCommand(txt.split(' ')[0])+' '+txt.split(' ')[1]))
        else:
                bot.sendMessage(msg['from']['id'],cmd.runAndReturn(cmd.getCommand(txt)))

    else:
        print "Comando nao encontrado: "+str(txt)
	bot.sendMessage(msg['from']['id'],"Comando nao encontrado "+str(txt))   

    flavor = telepot.flavor(msg)
    summary = telepot.glance(msg, flavor=flavor)
    print flavor, summary


TOKEN = "<TOKEN TELEGRAM>"
hash=MD5()
lastPic=hash.md5(IMG)
net=netUtil()

def alerts(self):
	for a in alert.getUsersOnMaxAlert("10"):
		print  bot.sendMessage(a[0],"alerta")
	
def sendImage():
        print "Sending img"
        f = open(IMG,'r')
        bot.sendPhoto('<TELEGRAM ID>',f)
	lastPic=hash.md5(IMG)	
        f.close();

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print 'Listening ...'

while 1:

	try:
    	    if not net.pingMAC("<MAC>"): 
		if not net.pingMAC("MAC"):
			print "Envio Liberado"
	    		pic=hash.md5(IMG)
	    		if pic != lastPic :
		    		print "Enviando..."
		    		sendImage()
		    		lastPic=pic
	    else:
		print "Desabilitado o envio"
    	except Exception as e:
    		print e
    	
