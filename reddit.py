#!/usr/bin/env python2.7
#  reddit.py  :  Parses a redditor's history to pull certain attributes, (un)popular comments/posts, and more...
#  Authors    :  Soonyoung Lim, Anthony Luc, and Donald Luc
#  Data Structures Final Project


# Import Modules:
import os
import sys
import requests
import re
import time
# Heap
import collections
from heapq import heappush, heappop, nlargest, nsmallest


# Define Variables:
USER = 'spez'
POSTS_PER_PAGE = 25
HEADERS  = {'user-agent': 'reddit-{}'.format(os.environ['USER'])}
TYPE = ''

# Heap Variables
NUMTOPBOT 	    = 3
COMMENTHEAP 	= []
POSTHEAP 		= []

# Define Dictionaries:
interests = {}
family = {}

# Define Object for use in the heap
myPair = collections.namedtuple('myPair', ['score', 'body'])

# Define Functions:
def usage(status):
	print '''Usage: {} ...
	-u USER	          The reddit user you wish to look up
	-n NUMTOP/BOT    The number of top and bottom comment/post scores'''.format(
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
			body = get_data(URL_JSON, i, 'body')
			
			score = get_data(URL_JSON, i, 'score')
			store_heap(score, body, TYPE)
			
			find_family(body)									# Grep For Comments Based On Family.

		# Get metadata for post/submitted.
		else:
			post_title = get_data(URL_JSON, i, 'title')
			self_post = get_data(URL_JSON, i, 'is_self')
			if self_post:
				body = get_data(URL_JSON, i, 'selftext')
				find_family(body)

			score = get_data(URL_JSON, i, 'score')
			store_heap(score, post_title, TYPE)
		
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

# Heap functions # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def store_heap(SCORE, BODY, TYPE):
	node = myPair(score = SCORE, body = BODY)
	if TYPE == 'comments':
		heappush(COMMENTHEAP, node)
	else: # submitted
		heappush(POSTHEAP, node)
    
# Print Functions
def print_top_bot(NUMTOPBOT=NUMTOPBOT):
	print "\n-----------------------------------------------------------------------"
	print "Top", NUMTOPBOT, "Comments:"
	a = nlargest(NUMTOPBOT, enumerate(COMMENTHEAP), key=lambda x: x[1])
	print_heap(a, 'comments')
	print "\n-----------------------------------------------------------------------"
	print "Bottom", NUMTOPBOT, "Comments:"
	a = nsmallest(NUMTOPBOT, enumerate(COMMENTHEAP), key=lambda x: x[1])
	print_heap(a, 'comments')
	print "\n-----------------------------------------------------------------------"
	print "Top", NUMTOPBOT, "Posts:"
	a = nlargest(NUMTOPBOT, enumerate(POSTHEAP), key=lambda x: x[1])
	print_heap(a, 'submitted')
	print "\n-----------------------------------------------------------------------"
	print "Bottom", NUMTOPBOT, "Posts:"
	a = nsmallest(NUMTOPBOT, enumerate(POSTHEAP), key=lambda x: x[1])
	print_heap(a, 'submitted')

def print_heap(heap, TYPE=TYPE):   # Function that prints the heap
	for k,v in enumerate(heap):
		if TYPE == 'comments':
			print "\nComment: #{}\tScore: {}\n{}\n".format(k+1, v[1][0], v[1][1].rstrip())
		else:
			print "\nPost: #{}\tScore: {}\nTitle: {}\n".format(k+1, v[1][0], v[1][1].rstrip())

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def print_interests():
	print '\n'
	print USER+'\'s interests are:'
	print '------------------------------------------'
	print '| {:>20} | {:>15} |'.format("interest","# of occurences")
	print '------------------------------------------'
	for i in sorted(interests, key=interests.get, reverse=True)[:10]:
		print '| {:>20} | {:>15} |'.format(i,interests[i])
		print '------------------------------------------'

def print_family():
	print '\n'
	print USER+' has :'
	print '------------------------------------------'
	print '| {:>20} | {:>15} |'.format("family member", "# of occurences")
	print '------------------------------------------'
	for f in sorted(family, key=family.get, reverse=True):
		print '| {:>20} | {:>15} |'.format(f,family[f])
		print '------------------------------------------'

def print_time(start_time):
	print("--- %s seconds ---" % (time.time() - start_time))

# Main Execution:
if __name__ == '__main__':
	start_time = time.time()
	args = sys.argv[1:]
	while len(args) and args[0].startswith('-') and len(args[0]) > 1:
		arg = args.pop(0)
		if arg == '-h':
			usage(0)
		elif arg == '-n':
			NUMTOPBOT = int(args.pop(0))
		elif arg == '-u':
			USER = args.pop(0)
		else:
			usage(1)

	print("Parsing through comments and posts...")

	# Get Comments / Posts:
	TYPE = 'comments'
	parse_user_history(TYPE)
	TYPE = 'submitted'
	parse_user_history(TYPE)

	print("Printing results...")

	# Print Overview:
	print_top_bot(NUMTOPBOT)
	print_interests()
	print_family()
	print_time(start_time)
