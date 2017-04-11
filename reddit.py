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
user = 'madviet'
page_count = '25'

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

# Get Posts:
web_address = 'https://www.reddit.com/u/'+user+'/comments/.json'
url = requests.get(web_address,headers=headers).json()
comment = url["data"]["children"][0]["data"]["body"] # Saves the pointer to the next page.
print comment

'''while (next_page):
	print next_page
	web_address = 'https://www.reddit.com/u/'+user+'/submitted/?count='+page_count+'&after='+next_page
	url = requests.get(web_address,headers=headers).json()
	next_page = url["data"]["after"]'''

'''i = 0
tryval = 1;
while tryval:
	try:
		title = url["data"]["children"][i]["data"]["link_title"]
		link_author = url["data"]["children"][i]["data"]["link_author"]
		author = url["data"]["children"][i]["data"]["author"]
		#body = url["data"]["children"][i]["data"]["body"]
		#subreddit = url["data"]["children"][i]["data"]["subreddit"]
		if author == link_author:
			print "This is a post"
			print title	
		
		print "Title: "+title
		print "Link Author: "+link_author
		print "Author: "+author
		print "Body: "+body
		print "Subreddit: "+subreddit
		
	except KeyError:
		#print "error"
		tryval = 0
		#sys.exit(1)
	i = i + 1'''

