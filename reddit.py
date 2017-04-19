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
USER = '3yearold'
POSTS_PER_PAGE = 25
HEADERS  = {'user-agent': 'reddit-{}'.format(os.environ['USER'])}


# Define Functions:
def usage(status):
	print '''Usage: {} -u USER
	-u USER		The reddit user you wish to look up'''.format(
		os.path.basename(sys.argv[0])
	)
	sys.exit(status)

def get_data(URL_JSON, INDEX, DATA):
	return URL_JSON['data']['children'][INDEX]['data'][DATA]

def get_initial_page(TYPE):
	web_address = 'https://www.reddit.com/u/{}/{}/.json'.format(USER, TYPE)
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


# Get Comments:
'''
post_or_comment = 'comments'

next_page = get_initial_page(post_or_comment)
count = POSTS_PER_PAGE
while (next_page):
	next_page = get_next_page(post_or_comment, count, next_page)
	count = count + POSTS_PER_PAGE'''

  
web_address = "https://www.reddit.com/u/"+USER+"/comments/.json"
url_json = requests.get(web_address,headers=HEADERS).json()
interests = {}
family = {}

for i in range(0, len(url_json["data"]["children"])):
	# Get Metadata.
	link_title = get_data(url_json, i, 'link_title')
	link_author = get_data(url_json, i, 'link_author')
	author = get_data(url_json, i, 'author')
	body = get_data(url_json, i, 'body')
	subreddit = get_data(url_json, i, 'subreddit')

	# age
        #regex = r"I'm +\d+ years old"
	#matches = re.findall(regex, body)
	matches = re.findall(r"son", body)
        for match in matches:
                print match

	# Grep For Comments Based On Family.
	f = open("family.txt")
	for word in f.readlines():
		word = word.strip();
		if (re.search(word, body)):
			if word in family:
                            family[word] = family[word] + 1
                        else:
                            family[word] = 1

	# user's interests
	if subreddit in interests:
		interests[subreddit] = interests[subreddit] + 1
	else:
		interests[subreddit] = 1

	# print
	'''
	print "Link Title: "+link_title
	print "Link Author: "+link_author
	print "Author: "+author
	print "Body: "+body
	print "Subreddit: "+subreddit
	print "----------------------------------"
	'''
'''
print USER+'\'s interests are:'
for key, value in interests.items():
	print '{}\t{}'.format(key, value)

print USER+' has :'
for key, value in family.items():
        print '{}\t{}'.format(key, value)
'''
