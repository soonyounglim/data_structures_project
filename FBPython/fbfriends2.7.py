#!/usr/bin/env python2.7
#Author  :  Donald Luc

import json
import os
import base64
import urllib
import urllib2

url = 'https://graph.facebook.com/v2.8/me/photos'
facebook_api_key = raw_input("Please enter your FB API Key: ")


headers = {'Authorization': 'Bearer {}'.format(facebook_api_key)}
request = urllib2.Request(url, headers)

encoding = urllib.urlencode(headers)
print(type(request))
#response = urllib2.urlopen(request)

'''
if encoding is None:
	print('No encoding.')
	encoding = 'utf-8'


data = json.loads(response.read().decode(encoding))
data = data['data']
print(len(data))
'''