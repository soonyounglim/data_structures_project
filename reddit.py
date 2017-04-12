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