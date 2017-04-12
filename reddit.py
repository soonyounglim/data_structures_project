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
HEADERS  = {'user-agent': 'reddit-{}'.format(os.environ['USER'])}
USER = 'spez'
POSTS_PER_PAGE = 25

# Define Functions:
def usage(status):
	print '''Usage: {} -u USER
	-u USER		The reddit user you wish to look up'''.format(
		os.path.basename(sys.argv[0])
	)
	sys.exit(status)

def get_initial_page(TYPE):
	web_address = 'https://www.reddit.com/u/{}/submitted/.json'.format(USER)
	url = requests.get(web_address,headers=HEADERS).json()
	print web_address
	return url["data"]["after"] # Saves the pointer to the next page.

def get_next_page(TYPE, COUNT, NEXT_PAGE):
	web_address = 'https://www.reddit.com/u/{}/{}/.json?count={}&after={}'.format(USER, TYPE, COUNT, NEXT_PAGE)
	url = requests.get(web_address,headers=HEADERS).json()
	print web_address
	return url['data']['after']

# Main Execution:
args = sys.argv[1:]
while len(args) and args[0].startswith('-') and len(args[0]) > 1:
	arg = args.pop(0)
	if arg == '-h':
		usage(0)
	elif arg == '-u':
		USER = args.pop(0)
	else:
		usage(1)


# Get Posts:
next_page = get_initial_page('submitted')
count = POSTS_PER_PAGE
while (next_page):
	next_page = get_next_page('submitted', count, next_page)
	count = count + POSTS_PER_PAGE

  
comments_web_address = "https://www.reddit.com/u/"+user+"/comments/.json"
comments_url = requests.get(comments_web_address,headers=headers).json()
interests = {}
family = {}

for i in range(0, len(comments_url["data"]["children"])):
	link_title = comments_url["data"]["children"][i]["data"]["link_title"]
	link_author = comments_url["data"]["children"][i]["data"]["link_author"]
	author = comments_url["data"]["children"][i]["data"]["author"]
	body = comments_url["data"]["children"][i]["data"]["body"]
	subreddit = comments_url["data"]["children"][i]["data"]["subreddit"]
	f = open("family.txt")
	for word in f.readlines():
		word = word.strip();
		if (re.search(word, body)):
			if word in family:
                            family[word] = family[word] + 1
                        else:
                            family[word] = 1

	if subreddit in interests:
		interests[subreddit] = interests[subreddit] + 1
	else:
		interests[subreddit] = 1
	'''
	print "Link Title: "+link_title
	print "Link Author: "+link_author
	print "Author: "+author
	print "Body: "+body
	print "Subreddit: "+subreddit
	print "----------------------------------"
	'''
print user+"'s interests are: "
for key, value in interests.items():
	print key, value

print user+" has :"
for key, value in family.items():
        print key, value
