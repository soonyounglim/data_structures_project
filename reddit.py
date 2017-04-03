#!/usr/bin/env python2.7

import os
import sys
import requests
import re

headers  = {'user-agent': 'reddit-{}'.format(os.environ['USER'])}

def usage(status=0):
    print '''Usage: reddit.py [ -f FIELD -s SUBREDDIT ] regex
    -f FIELD        Which field to search (default: title)
    -n LIMIT        Limit number of articles to report (default: 10)
    -s SUBREDDIT    Which subreddit to search (default: linux)'''.format(
        os.path.basename(sys.argv[0]), FIELD, LIMIT, SUBREDDIT
    )
    sys.exit(status)

# Global variables
LIMIT = 10
USER = "madviet"
FIELD = ""
SUBREDDIT = ""


args = sys.argv[1:]

while len(args) and args[0].startswith('-') and len(args[0]) > 1:
    arg = args.pop(0)
    if arg == '-f':
        FIELD = str(args.pop(0))
    elif arg == '-n':
    	LIMIT = int(args.pop(0))
    elif arg == '-s':
        SUBREDDIT = str(args.pop(0))
    elif arg == '-h':
    	usage(0)
    else:
    	usage(1)

if len(args):
	REGEX = str(args.pop(0))
else:
	REGEX = ""

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
