from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
import urllib2
import json
import datetime
from django.utils.dateformat import format

day = 86400
base_url_0 = "http://chart.apis.google.com/chart?cht=lc&chd=t:"
base_url_1 = "0,0&chds=0,6&chls="
base_url_2 = "&chs=1000x125&chm="

# "http://chart.apis.google.com/chart?cht=lc&chd=t:1,2,1,3,5,3,1,1,4,3,1,1,3,5,3,1,1,0,0,01,2,1,3,5,3,1,1,4,3,1,1,3,5,3,1,1,0,0,0|0,0&chds=0,6&chls=0,1,0&chs=1000x125&chm=b,99ff00,0,1,0" 

# "http://chart.apis.google.com/chart?cht=lc&chd=t:1,2,1,3,5,3,1,1,4,3,1,1,3,5,3,1,1,0,0,01,2,1,3,5,3,1,1,4,3,1,1,3,5,3,1,1,0,0,0|0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0|0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0|0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0|0,0&chds=0,6&chls=0,1,0|0,1,0|0,1,0|0,1,0|0,1,0|0,1,0&chs=1000x125&chm=b,99ff00,0,1,0|b,ffff00,1,2,0|b,ff9900,2,3,0|b,ff3300,3,4,0"


import urllib

base_url = 'https://gimmebar.com/api/v0'
client_id = '4eab0fb02e0aaae406000031'
client_secret = '5e8c86bf6f93caf9c4da649303607fca'

# AUTHENTICATE THE USER
def landing(request):
	return render_to_response('graphs/index.html',context_instance=RequestContext(request))

def authenticate(request):
	# STEP 1: Generate a request token
	post_url = '/auth/reqtoken'
	params = urllib.urlencode({'client_id': client_id, 'client_secret':client_secret, 'type':'app'})
	data = urllib2.urlopen('%s%s' % (base_url, post_url), params).read()
	data = json.loads(data)
	url = "https://gimmebar.com/authorize?client_id="+client_id+"&token="+data['request_token']+"&response_type=code"
	updates = {'url': url}
	print updates
	return HttpResponse(json.dumps(updates), mimetype="application/json")
	
def graphs(request):
	now = format(datetime.datetime.now(), u'U')
	response = urllib2.urlopen('https://gimmebar.com/api/v0/public/assets/tmincey/assorted-awesome?limit=50')
	html = response.read()
	obj = json.loads(html)
	count = 0
	last_count = 0
	final_url = base_url_0
	days = []
	for r in obj['records']:
		difference = int(now) - int(r['date'])
		while day < difference:
			count = count + 1
			difference = difference - day						
		#everyday needs to be marked, so look for each mark
		days.append(count)
		last_count = count
		count = 0
	day_string = ""
	for x in reversed(range(0,days[len(days)-1]+1)):
		for d in days:
			if d == x:
				count = count + 1
		if x == 0:
			day_string = day_string + str(count)
		else:
			day_string = day_string + str(count) + ","
		count = 0
	print day_string
# 	for x in range(0,3):
	return render_to_response('graphs/graphs.html',context_instance=RequestContext(request))
	

	
	
	