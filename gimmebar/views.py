from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
import urllib
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


# Information about the Gimme API 
# https://gimmebar.com/api/v0

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
	token = data['request_token']
	url = "https://gimmebar.com/authorize?client_id="+client_id+"&token="+token+"&response_type=code"
	updates = {'url': url, 'token':token}
	# STEP 2:
	return HttpResponse(json.dumps(updates), mimetype="application/json")

def exchange(request):
	token = request.GET.get('token', '')
	# STEP 3: Exchange the request token for an authorization token when the user returns
	post_url = '/auth/exchange/request'
	params = urllib.urlencode({'client_id': client_id, 'token':token, 'response_type':'code'})
	data = urllib2.urlopen('%s%s' % (base_url, post_url), params).read()
	data = json.loads(data)
	code = data['code']
	# STEP 4: Exchange the authorization token for an access token
	post_url = '/auth/exchange/authorization'
	params = urllib.urlencode({'code': code,'grant_type':'authorization_code'})
	data = urllib2.urlopen('%s%s' % (base_url, post_url), params).read()
	data = json.loads(data)
	access_token = data['access_token']
	# STEP 5: Use the access token to authenticate with the API and retrieve user data
	print access_token
	post_url = '/collections'
	headers = {'Authorization': 'Bearer %s' % access_token}
	params = urllib.urlencode({})
	full_url = '%s%s' % (base_url, post_url)
	req = urllib2.Request(full_url, headers=headers)
	response = urllib2.urlopen(req)
	html = response.read()
	obj = json.loads(html)
	
# 	CREATE THE PIE CHART URL AND INFO
	graph_base = 'http://chart.apis.google.com/chart?cht=p&chd=t:'
	graph_middle = ''
	graph_end = '&chco=ff3300&chs=300x300&chf=bg,s,EFEFEF00'
	
	collection_list = []
	categories = []
	
# 	create the list of data for the pie chart
	for o in obj:
		try:
			collection_list.append(len(o['assets']))
			categories.append({'title':o['title'],'amount':len(o['assets'])})
		except:
			collection_list.append(0)
			categories.append({'title':o['title'],'amount':0})

	collection_list.sort()
	collection_list.reverse()
	first = True
	
# 	turn the list into a string of data with commas
	for x in collection_list:
		if first is True:
			graph_middle = str(x)
			first = False
		else:
			graph_middle = graph_middle+','+str(x)
	graph_url = graph_base + graph_middle + graph_end
	print graph_url
	return render_to_response('graphs/exchange.html',{'graph_url':graph_url,'categories':categories},context_instance=RequestContext(request))
# <div class="image" id="medium"><div class="subtitle">1. categories</div><img src="http://chart.apis.google.com/chart?cht=p&chd=t:100,33,25,19,12,8,6,6,5,3,3,2,2,2,2,1,0,0,0,0&chco=ff3300&chs=150x150&chf=bg,s,EFEFEF00" alt="pie" style="margin-right:40px;"/></div>


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
	

	
	
	