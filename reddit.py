#!/usr/bin/env python2.7
#  reddit.py  :  Parses a redditor's history to pull certain attributes, (un)popular comments/posts, and more...
#  Authors    :  Soonyoung Lim, Anthony Luc, and Donald Luc
#  Data Structures Final Project


# Import Modules:
import os
import sys
import requests
import re


# Define Variables:
headers  = {'user-agent': 'reddit-{}'.format(os.environ['USER'])}
user = "madviet"
web_address = "https://www.reddit.com/u/"+user+"/.json"


# Define Functions:
def usage(status):
	print '''Usage: {} -u USER
	-u USER		The reddit user you wish to look up'''.format(
		os.path.basename(sys.argv[0])
	)
	sys.exit(status)


# Main Execution:
args = sys.argv[1:]
while len(args) and args[0].startswith('-') and len(args[0]) > 1:
	arg = args.pop(0)

	if arg == '-h':
		usage(0)
	elif arg == '-u':
		user = args.pop(0)
	else:
		usage(1)

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
