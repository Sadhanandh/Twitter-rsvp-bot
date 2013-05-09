
from xml.dom import minidom
import xml.parsers
import mechanize
import glob
import os
import time
import mob
file_cap = "caption.txt"
diclocat = "dict"
logfile = "mylog"

def mainer(location):
	dic = []
	if  os.path.isfile(diclocat):
		f = open(diclocat)
		for x in f.readlines():
			dic.append(x.strip("\n"))
		f.close()

	files = glob.glob(os.path.join(location,"*.xml"))
	print files
	for filen in files:
		if filen not in dic:
			xmlopener(filen)
			dic.append(filen)
			f = open(diclocat,"w")
			f.write("\n".join(dic)+"\n")
			f.close()

def xmlopener(filename):
	f=open(file_cap)
	caption = f.read()
	f.close()
	logw = open(logfile,"a")
	t_t =time.strftime("%d-%m-%Y %H:%M")
	logw.write("--------"+t_t+"---------\n")
	try:
		xmldoc = minidom.parse(filename)
		tag = xmldoc.getElementsByTagName("Facebook")
		log_n = tag[0].attributes['login'].value
		pass_w = tag[0].attributes['password'].value
		tag = xmldoc.getElementsByTagName("Picture")
		locat = tag[0].attributes['filename'].value
		try:
			mob.login(log_n,pass_w,locat,caption)
		except IOError:
			print "Failed!!"
			logw.write("Failed!! - File not found "+log_n+" "+locat+"\n")
		except mechanize._form.ControlNotFoundError:
			print "Failed!!"
			logw.write("Failed!! - Form not found "+log_n+" "+locat+"\n")
		except Exception:
			print "Failed!!"
			logw.write("Failed!! "+log_n+" "+locat+"\n")
		#print log_n,pass_w,locat,caption
	except KeyError:
		print "Not found."
		logw.write("XML Error - Login Not found\n")
	except IndexError:
		print "Not found."
		logw.write("XML Error - Facebook Not found\n")
	except xml.parsers.expat.ExpatError:
		print "Not Found."
		logw.write("XML Error -  Elements Not found\n")
