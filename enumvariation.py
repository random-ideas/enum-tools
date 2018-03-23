#!/usr/bin/python

import sys
import urllib2
import getopt
#this relies on signal for timeouts, there is NOT a way to make that work in windows
#this is from http://stackoverflow.com/questions/2281850/timeout-function-if-it-takes-too-long-to-finish
from functools import wraps
import errno
import os
import signal

class TimeoutError(Exception):
    pass

def timeout(seconds=5, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wraps(func)(wrapper)
    return decorator

def main(argv):
	url = ''
	try: #so far only using u U as an input
		opts, args = getopt.getopt(argv, "hu:U:",["url="])
	except getopt.GetoptError:
		print "program.py -u url"
	for opt, arg in opts:
		if opt == '-h':
			print "program.py -u url"
			sys.exit()
		elif opt in ("-u", "-U", "url"):
			#TODO ADD CHECKING IN HERE
			url = arg	
	print "Url to test", url
	print "Testing!"
	buildURLList(url)

def buildURLList(url):
	req = urllib2.Request(url)
	# Unused for now, but test localhost behaviour in future
	# req.add_header('Referrer', 'localhost')
	#hardcoded user agent for now, will make an input file later
#	userAgents = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36", "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0", "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0", "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; Trident/5.0)"]
	userAgents = ["Chrome Win7", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36", "Chrome Win8.1", "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36", "Chrome Win10", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36", "Safari OSX", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14", "Chrome OSX", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36", "Chrome Linux", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36", "Firefox Linux", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0", "Firefox Win10", "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0", "Firefox Win7", "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36", "Safari - iOS", "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1", "Android 6 Chrome", "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 6P Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36"]
#	for index, agent in enumerate(userAgents)[::2]:
	# set to one as it's the first user agent, 0 is description
	lineIndex = 1
	#loop to iterate through user agent list, make request, get length and return it
	while lineIndex < len(userAgents):
		agent = userAgents[lineIndex]
		req.add_header('User-Agent', agent)
		req.add_header('Referrer', url)
		try:
			response = requestURL(req)
			print "Response length for " + userAgents[lineIndex-1] + " is: " + str(len(response))
		except urllib2.HTTPError as e:
			print("HTTP Response " + str(e) + " for User agent " + userAgents[lineIndex-1])
		except:
			#needs better error handling
			print("Site is either down or other issue identified for User agent " + userAgents[lineIndex-1])
		lineIndex += 2
@timeout()
def requestURL(req):
	return urllib2.urlopen(req).read()


if __name__ == "__main__":
	main(sys.argv[1:])
