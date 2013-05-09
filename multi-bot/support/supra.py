#!/usr/bin/env python 
import tweepy
import os
import sys
import Queue
import threading


consumer_key = 	"LqGNNFbT96Qhtwybnk5pSQ"
consumer_secret = "o9WH1xNOZeAjevlFNWgfAf3kQpt0knzXuMSx78GytmY"

def checkauth():
	db = readdb()
	dic = {}
	if os.path.isfile("keys"):
		dic = readkeys()
	for x in db:
		if not x in dic:
			print "Authentication Phase not complete.."
			print "1 - Stage 1"
			print "2 - Stage 2"
			ch = raw_input("Enter your choice : ")
			if ch == "1":
				prea()
			else:
				if os.path.exists("tempkeys"):
					dic = readtempkeys()
					posta(dic)
				else:
					print "Wrong choice . please complete stage 1"
			sys.exit()

	else:
		return True

def prea():

## Getting access key and secret
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth_url = auth.get_authorization_url()
	e_mail=raw_input("Email of the person whom you intend to send: ")
	print "Mail the person this url for him to AUTHORIZE the app"
	print " "
	print "   mailto :",e_mail," : ----- ",auth_url
	print ""
	print "Once you recieve the authorization pin,you can continue with the next step"
	print ""
	ff=open("urls","a")
	ff.write(e_mail+" : "+auth_url+os.linesep)
	ff.close()


	access_key = auth.request_token.key
	access_secret = auth.request_token.secret
	if not os.path.isfile("tempkeys"):
		f = open("tempkeys","w")
	else :
		f = open("tempkeys","a")
	f.write(str(e_mail) +","+access_key+","+access_secret+"\n")
	f.close()



def posta(dic):

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	try :
		se_nu = raw_input('The email-ID  of the senders PIN:')
		verifier = raw_input('PIN: ').strip()
		try:
			a1,a2 = dic[se_nu]
			auth.set_request_token(a1,a2)
			auth.get_access_token(verifier)
			access_key = auth.access_token.key
			access_secret = auth.access_token.secret
			api = tweepy.API(auth)
			s_name = api.me().screen_name
			print "Authentication done"
			if not os.path.isfile("keys"):
				f = open("keys","w")
			else :
				f = open("keys","a")
			f.write(s_name +","+access_key+","+access_secret+"\n")
			f.close()
		except KeyError :
			print "Serial not found!! check your serial"


	except tweepy.error.TweepError as e:
		print "Not Authenticated!!",e


def makeapis(consumer_key = consumer_key, consumer_secret = consumer_secret ):
	apidic = {}
	dic = readkeys()
	db = readdb()
	for name in db:
		try : 
			access_key,access_secret = dic[name]
			auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
			auth.set_access_token(access_key, access_secret)
			api = tweepy.API(auth)
			print api.me().screen_name,"Authentication initialised"
			fname,shsize = db[name]
			mytext = " ,"+fname+", Size "+shsize
			apidic[name]=[api,mytext]
		except KeyError:
			print "Key not found"
			print "User not found! Did you authenticate this user?"
		except tweepy.error.TweepError as e:
			print "Authentication error!!" ,e
		except Exception as e:
			print "Error",e
	return apidic

def readkeys():

	dic = {}
	f = open("keys")
	for data in f.readlines():
		s_name,access_key,access_secret = data.strip("\n").split(",")
		dic[s_name]=[access_key,access_secret]
		#if len(dic)>10:
		#	break
	f.close()
	return dic

def readtempkeys():

	dic = {}
	f = open("tempkeys")
	for data in f.readlines():
		nu,a1,a2 = data.strip("\n").split(",")
		dic[nu]=[a1,a2]
	f.close()
	return dic


def readdb():
	db = {}
	f  = open("usersdb")
	for x in f.readlines():
		x = x.strip("\n").split(",")
		try :
			db[x[0].strip().strip('@')]=[x[1].strip(),x[2].strip()]
		except IndexError:
			print "check your usersdb file !!"
		if len(db)>10:
			break
	return db



def runner(to_name,textme,Q):
	apit = Q.get()
	name,api,ftext = apit
	sendtext = textme+ftext
	#print name,"Sending..."
	try:
		api.send_direct_message(screen_name="@"+to_name,text = sendtext)
	except Exception :
		print "Retrying"
		try:
			api.send_direct_message(screen_name="@"+to_name,text = " "+sendtext)
		except Exception :
			print "Failed"
	print name+" Sent the message "+sendtext
	Q.task_done()


def demorunner(to_name,text,Q):
	a,b,c = Q.get()
	print a+" "+b+" "+c
	Q.task_done()

def procedure(apidic,text,to_name):
	fetch_parallel(apidic,to_name,text)

def fetch_parallel(apidic,to_name,text):
	Q = Queue.Queue()
	for x in apidic:
		api,ftext = apidic[x]
		host = (x,api,ftext)
		Q.put(host)
	threads = [threading.Thread(target=runner, args = (to_name,text,Q)) for url in apidic]
	for t in threads:
		t.start()
	for t in threads:
		t.join()
