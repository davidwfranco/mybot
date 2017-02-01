# -*- coding: utf-8 -*-
import urllib2
import sys
import os
import json
from HTMLParser import HTMLParser
from StringIO import StringIO
reload(sys)
sys.setdefaultencoding('utf8')
#https://api.blinktrade.com/api/v1/BRL/ticker
class Cotacao(object):
	
	def getCurrencyInfo(self,currency):
		try:
		
			#currency=str(sys.argv[1]).upper()
			#request = urllib2.Request("http://api.promasters.net.br/cotacao/v1/valores?moedas="+currency+"&alt=json")
			request = urllib2.Request("https://api.blinktrade.com/api/v1/BRL/ticker")
			request.add_header('Accept-enconding', 'gzip')
			response = urllib2.urlopen(request)
			data=""
			if response.info().get('Content-Encoding') == 'gzip':
				buf = StringIO(response.read())
				f = gzip.GzipFile(fileobj=buf)
				data = f.read()
			else:
				data = response.read()
			j=json.loads(data)
			
			return j#open('./valor').readlines()	
			#rint "1 "+j['valores'][currency]['nome']+" = "+str("{0:.2f}".format(j['valores'][currency]['valor']))+" reais\n"+j['valores'][currency]['fonte']
		except Exception as e:
			print "Moeda desconhecida, tente USD,GPB,BTC ou ARS" 
			print e
	
	
	def getCurrencyValue(self,currency):
		j=self.getCurrencyInfo(currency)
		#return j['valores'][currency.upper()]['valor']
		return j['last']#[currency.upper()]['valor']
		#return open('./valor').readlines()[0].rstrip('\n')#j['valores'][currency.upper()]['valor']
