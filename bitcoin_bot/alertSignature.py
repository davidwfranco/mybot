# -*- coding: utf-8 -*-
import sqlite3
import os,time,re
import subprocess as sp
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

DATABASE="/opt/scripts/bitcoin_bot/alertSignature.db"
TABLE="ACCOUNTS"
CONN=None

class AlertSignature(object):

	
	def getConnection(self):
		if CONN == None:
			return sqlite3.connect(DATABASE,isolation_level=None)
		else:
			return CONN
		#return sqlite3.connect(DATABASE)
	
	def getCursor(self):
		CONN = self.getConnection()
		return CONN.cursor()
		
	def dbConfig(self):
                (self.getCursor()).execute("create table "+TABLE+" (uid integer primary key,currency text,max real,nmax real, min real,nmin real,period int, last_alert date)")
		(self.getCursor()).execute("insert into ACCOUNTS values (0,0,0,0,0,0,0,0)")
		self.commit()

	def commit(self):
		#print "Commit"
		CONN = self.getConnection()
		if CONN is None:
			print "Erro conexao!"
		#else: 
			#print CONN
		CONN.commit()
		CONN.close();

	def signup(self,uid):
		#print "signup"+uid
		self.getCursor().execute("insert into "+TABLE+" (uid) values (?)",[uid])
                statement="update %s set currency=? where uid=?" %(TABLE)
                self.getCursor().execute(statement,("BTC",uid))
		self.commit()

	def turnOff(self,uid):
		print "turnoff"

	def getStatus(self,uid):
		print "getStatus"

	def setMinCurrencyValue(self,uid,value):
		#print "setMinCurrencyValue"
                statement="update %s set min=? where uid=?" %(TABLE)
                self.getCursor().execute(statement,(value,uid))
                self.commit()

	def setMaxCurrencyValue(self,uid,value):
		#print "setMaxCurrencyValue"
                statement="update %s set max=? where uid=?" %(TABLE)
                self.getCursor().execute(statement,(value,uid))
                self.commit()

	def setPeriod(self,uid,period):
		#print "setPeriod "+uid+" "+period
		statement="update %s set period=? where uid=?" %(TABLE)
		self.getCursor().execute(statement,(period,uid))
		self.commit()

	def getUsersOnMaxAlert(self,max):
		#print "getUsersOnMaxAlert"
                statement="select uid from %s where max<=?" %(TABLE)
                ret=self.getCursor().execute(statement,[max]).fetchall()
		return ret

	def getUsersOnMinAlert(self,min):
		#print "getUsersOnMinAlert"
		statement="select uid from %s where min>=?" %(TABLE)
                ret=self.getCursor().execute(statement,[min]).fetchall()
                return ret
	
	def getUserLastAlert(self,uid):
		statement="select last_alert from %s where uid=?" %(TABLE)
		ret=self.getCursor().execute(statement,[uid]).fetchone()
                return ret

	def setUserLastAlert(self,uid):
		statement="update %s set last_alert=? where uid=?" %(TABLE)
		self.getCursor().execute(statement,(time.time(),uid))
		self.commit()
	def getMinCurrencyValue(self,uid):
		statement="select min from %s where uid=?" %(TABLE)
		ret=self.getCursor().execute(statement,[uid]).fetchone()
		return ret

	def getMaxCurrencyValue(self,uid):
		statement="select max from %s where uid=?" %(TABLE)
		ret=self.getCursor().execute(statement,[uid]).fetchone()
		return ret
