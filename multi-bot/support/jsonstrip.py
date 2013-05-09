#import json
try:
    import json
except ImportError:
    import simplejson as json 
import urllib

def extract(u_name):
	d = urllib.urlopen("https://api.twitter.com/1/users/show.json?screen_name="+u_name.strip("@"))
	html = d.read()
	j = json.loads(html)
	try:
		u_id =j["id_str"]
		return u_id
	except KeyError: 
		print "Doesnt exist"
		return None

