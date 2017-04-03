#!/usr/bin/env python2.7

import os
import sys
import requests
import re
test update...

headers  = {'user-agent': 'reddit-{}'.format(os.environ['USER'])}

USER = "madviet"

web_address = "https://www.reddit.com/u/"+USER+"/.json"
url = requests.get(web_address,headers=headers).json()

print url

'''COUNT = 1
i = 0
while COUNT <= LIMIT:
	title = url["data"]["children"][i]["data"]["title"]
	author = url["data"]["children"][i]["data"]["author"]
	link = url["data"]["children"][i]["data"]["url"]
	try:
		string = url["data"]["children"][i]["data"][FIELD]
	except KeyError:
		print "Invalid field: {}".format(FIELD)
		sys.exit(1)
	possible = re.findall(REGEX, string)
	if possible:
		print COUNT, ".",
		print "\tTitle: \t", title
		print "\tAuthor: ", author
		print "\tLink: \t", link
		COUNT = COUNT + 1
	i = i + 1
'''
