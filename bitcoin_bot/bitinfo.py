#!/usr/bin/python2
import sys
import time
import telepot
from commandParser  import CommandParser
from account        import Account
from alertSignature import AlertSignature
from Cotacao_Foxbit import Cotacao
from md5	    import MD5
cmd = CommandParser()
account = Account()
alert = AlertSignature()
cotacao = Cotacao()

def handle(msg):

	
    txt = str(msg['text']).lower().replace(';',' ')
    print str(msg)
    if txt == "saldo":
		balance = account.getBalance(msg['from']['id'])
		bot.sendMessage(msg['from']['id'],balance)
		
    elif txt.startswith("debito"):
		print "Debito: "+txt.split(' ')[1]
		account.doDebit(txt.split(' ')[1],str(msg['from']['id']))
		balance = account.getBalance(msg['from']['id'])
		bot.sendMessage(msg['from']['id'],balance)
		
    elif txt.startswith("credito"):
		print "credito: "+txt.split(' ')[1]
		account.doCredit(txt.split(' ')[1],str(msg['from']['id']))
		balance = account.getBalance(msg['from']['id'])
		bot.sendMessage(msg['from']['id'],balance)


    elif cmd.getCommand(txt):
        print "Nao conheco a palavra "+str(cmd.getCommand(txt))+" envie ajuda para conhecer os comando possiveis"
        if len(txt.split(' ')) > 1:
                bot.sendMessage(msg['from']['id'],cmd.runAndReturn(cmd.getCommand(txt.split(' ')[0])+' '+txt.split(' ')[1]))
        else:
                bot.sendMessage(msg['from']['id'],cmd.runAndReturn(cmd.getCommand(txt)))

    elif txt == "alerta":
	bot.sendMessage(msg['from']['id'],"Envie assinar para receber alertas de bitcoin")

    elif txt == '/start':
	bot.sendMessage(msg['from']['id'],"Bem vindo, envie \"ajuda\" para conhecer saber o que posso fazer por voce")
    elif txt == 'ajuda':
	bot.sendMessage(msg['from']['id'],"Envie cotacao <moeda> para consultar o valor atual de uma moeda, envie assinar para cadastrar um alerta de bitcoin, envie max <valor> para configurar o alerta de alta e min <valor> para definir um alerta de baixa")
	time.sleep(2)
	bot.sendMessage(msg['from']['id'],"Para consultar os valores cadatrados atualmente, envie min ou max")
	#bot.sendMessage(msg['from']['id'],cmd.getList())

    elif txt.startswith("max"):
	if len(txt.split(' '))>1:
		alert.setMaxCurrencyValue(msg['from']['id'],txt.split(' ')[1]) 
		bot.sendMessage(msg['from']['id'],"Alerta de valor maximo alterado para "+txt.split(' ')[1])
	else:
		bot.sendMessage(msg['from']['id'],"R$ "+str(alert.getMaxCurrencyValue(msg['from']['id'])[0]))

    elif txt.startswith("min"):
	if len(txt.split(' '))>1:
		alert.setMinCurrencyValue(msg['from']['id'],txt.split(' ')[1]) 
		bot.sendMessage(msg['from']['id'],"Alerta de valor minimo alterado para "+txt.split(' ')[1])
	else:
		bot.sendMessage(msg['from']['id'],"R$ "+str(alert.getMinCurrencyValue(msg['from']['id'])[0]))

    elif txt == "assinar":
	alert.signup(msg['from']['id']) 
	bot.sendMessage(msg['from']['id'],"Voce assinou alerta de bitcoin, envie max <valor> para cadastrar um alerta de alta ou min <valor> para cadastrar um alerta de baixa")

    else:
        print "Comando nao encontrado: "+str(txt)
	bot.sendMessage(msg['from']['id'],"Comando nao encontrado")   

    flavor = telepot.flavor(msg)
    summary = telepot.glance(msg, flavor=flavor)
    print flavor, summary


TOKEN = "<TOKEN TELEGRAM>"

def alerts(self):
	for a in alert.getUsersOnMaxAlert("10"):
		print  bot.sendMessage(a[0],"alerta")
	

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
#bot.message_loop(alerts)
print 'Listening ...'
btcold=cotacao.getCurrencyValue("btc")
hash=MD5()
# Keep the program running.
while 1:
	try:
	    time.sleep(60)
	    btc=cotacao.getCurrencyValue("btc")
	    print str(btc)+" "+str(btcold)
	    if btc>btcold:
		btcold=btc
    		#print "MAX"
    	        for a in alert.getUsersOnMaxAlert(btc):
    	    	#print alert.getUserLastAlert(a[0])[0]
		    #print "buscando max"
    		    if time.time()-alert.getUserLastAlert(a[0])[0]>600:
			#print "Enviando max"
    			bot.sendMessage(a[0], "Valor do Bitcoin em ALTA: \nR$"+str(btc))
    			alert.setUserLastAlert(a[0])
    	    if btc<btcold:
		#print "MIN"
		btcold=btc	
		#print alert.getUsersOnMinAlert(btc)
    	        for b in alert.getUsersOnMinAlert(btc):
		    #print "buscando min"
    		    if time.time()-alert.getUserLastAlert(b[0])[0]>600:
			#print "enviando min"
    			bot.sendMessage(b[0], "Valor do Bitcoin em BAIXA: \nR$"+str(btc))
    			alert.setUserLastAlert(b[0])
    	except Exception as e:
    		print e
    	
