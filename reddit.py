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
USER = 'madviet'
POSTS_PER_PAGE = 25
HEADERS  = {'user-agent': 'reddit-{}'.format(os.environ['USER'])}
TYPE = ''

# Define Dictionaries:
interests = {}
family = {}


# Define Functions:
def usage(status):
	print '''Usage: {} -u USER
	-u USER		The reddit user you wish to look up'''.format(
		os.path.basename(sys.argv[0])
	)
	sys.exit(status)

def parse_user_history(TYPE):
	next_page = get_initial_page(TYPE)
	count = POSTS_PER_PAGE
	while (next_page):
		next_page = get_next_page(TYPE, count, next_page)
		count = count + POSTS_PER_PAGE

def parse_json(URL_JSON):	
	for i in range(0, len(URL_JSON["data"]["children"])):
		# Get metadata for comments.
		if (TYPE == 'comments'):
			comment_title = get_data(URL_JSON, i, 'link_title')
			comment_author = get_data(URL_JSON, i, 'link_author')
			body = get_data(URL_JSON, i, 'body')
			
			find_family(body)									# Grep For Comments Based On Family.

		# Get metadata for post/submitted.
		else:
			post_title = get_data(URL_JSON, i, 'title')
			self_post = get_data(URL_JSON, i, 'is_self')

			find_family(post_title)
		
		subreddit = get_data(URL_JSON, i, 'subreddit')


		# user's interests
		if subreddit in interests:
			interests[subreddit] = interests[subreddit] + 1
		else:
			interests[subreddit] = 1

def find_family(BODY):
	f = open("family.txt")
	for word in f.readlines():
		word = word.strip();
		if (re.search(word, BODY)):
			if word in family:
                            family[word] = family[word] + 1
                        else:
                            family[word] = 1


def get_data(URL_JSON, INDEX, DATA):
	return URL_JSON['data']['children'][INDEX]['data'][DATA]

def get_initial_page(TYPE):
	web_address = 'https://www.reddit.com/u/{}/{}/.json'.format(USER, TYPE)
	url = requests.get(web_address,headers=HEADERS).json()
	parse_json(url);
	return url["data"]["after"] # Saves the pointer to the next page.

def get_next_page(TYPE, COUNT, NEXT_PAGE):
	web_address = 'https://www.reddit.com/u/{}/{}/.json?count={}&after={}'.format(USER, TYPE, COUNT, NEXT_PAGE)
	url = requests.get(web_address,headers=HEADERS).json()
	parse_json(url);
	return url['data']['after']

def print_interests():
	print USER+'\'s interests are:'
	print '-------------------------------'
	print '{}\t{}'.format("interest","# of occurences")
	print '-------------------------------'
	for key, value in interests.items():
		print key
		for i in range(20-len(key)):
			print ' ',
		print value
		print '-------------------------------'

def print_family():
	print '\n'
	print USER+' has :'
	print '-------------------------------'
	print '{}\t{}'.format("family member", "# of occurences")
	print '-------------------------------'
	for key, value in family.items():
	        print '{}\t\t\t{}'.format(key, value)
		print '-------------------------------'

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


# Get Comments / Posts:
TYPE = 'comments'
parse_user_history(TYPE)
TYPE = 'submitted'
parse_user_history(TYPE)


# Print Overview:
print_interests()
print_family()
