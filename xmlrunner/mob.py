import mechanize
import cookielib
def login(log_n,pass_w,locat,caption):
# Browser
	br = mechanize.Browser()

# Cookie Jar
	cj = cookielib.LWPCookieJar()
	br.set_cookiejar(cj)

	br.set_handle_equiv(True)
#br.set_handle_gzip(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)

	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	br.open("https://m.facebook.com")
	br.select_form(nr=0)
	br.form["email"]=log_n
	br.form["pass"]=pass_w
	br.submit()

	br.open("https://m.facebook.com/upload.php")
	br.select_form(nr=0)
	print locat
	print locat[locat.rfind("/")+1:]
	br.form.add_file(open(locat),'text/plain',locat[locat.rfind("/")+1:])
	br.form.set_all_readonly(False)
	br.form["caption"]=caption
	br.submit()
# tags
	br.select_form(nr=0)
	br.submit()
