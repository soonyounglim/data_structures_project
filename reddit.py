#!/usr/bin/env python2.7
#  reddit.py  :  Parses a redditor's history to pull certain attributes, (un)popular comments/posts, and more...
#  Authors    :  Soonyoung Lim, Anthony Luc, and Donald Luc
#  Data Structures Final Project


# Import Modules:
import csv
import os
import sys
import requests
import re
import time
# Heap
import collections
from heapq import heappush, heappop, nlargest, nsmallest


# Define Variables:
USER              = 'spez'
POSTS_PER_PAGE    = 25
HEADERS           = {'user-agent': 'reddit-{}'.format(os.environ['USER'])}
TYPE              = ''
CSV               = False
PNG               = False
SILENT            = False

# Heap Variables
NUMTOPBOT 	      = 3
COMMENTHEAP 	  = []
POSTHEAP 		  = []

# Define Dictionaries:
interests         = {}
family            = {}
comment_scores    = {}
post_scores       = {}

# Define Object for use in the heap
myPair = collections.namedtuple('myPair', ['score', 'body'])

# Define Functions:
def usage(status):
	print '''Usage: {} ...
	-c               Create a csv file
	-n NUMTOP/BOT    The number of top and bottom comment/post scores
	-s SILENT        Silence output
	-p               Generate a barchart of data in a png
	-u USER	         The reddit user you wish to look up'''.format(
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
		subreddit = get_data(URL_JSON, i, 'subreddit')
		score = get_data(URL_JSON, i, 'score')
		
		# Get metadata for comments.
		if (TYPE == 'comments'):
			body = get_data(URL_JSON, i, 'body')
			store_heap(score, body, TYPE)
			subreddit_score(subreddit, score, TYPE)

			find_family(body)									# Grep For Comments Based On Family.

		# Get metadata for post/submitted.
		else:
			post_title = get_data(URL_JSON, i, 'title')
			self_post = get_data(URL_JSON, i, 'is_self')

			if self_post:
				body = get_data(URL_JSON, i, 'selftext')
				find_family(body)

			store_heap(score, post_title, TYPE)
			subreddit_score(subreddit, score, TYPE)

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
	print "Bottom", NUMTOPBOT, "Comments:"
	a = nsmallest(NUMTOPBOT, enumerate(COMMENTHEAP), key=lambda x: x[1])
	print_heap(a, 'comments')

	print "Top", NUMTOPBOT, "Posts:"
	a = nlargest(NUMTOPBOT, enumerate(POSTHEAP), key=lambda x: x[1])
	print_heap(a, 'submitted')

def print_heap(heap, TYPE=TYPE):   # Function that prints the heap
	for k,v in enumerate(heap):
		if TYPE == 'comments':
			print "#", k+1, "\tScore:", v[1][0], "\tComment:", v[1][1], "\n"
		else:
			print "#", k+1, "\tScore:", v[1][0], "\tTitle:", v[1][1], "\n"

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


def print_subreddit_comment_score():
	print '\n'
	print USER+' comment score in subreddit :'
	print '------------------------------------------'
	print '| {:>20} | {:>15} |'.format("Subreddit", "Score")
	print '------------------------------------------'
	for s in sorted(comment_scores, key=comment_scores.get, reverse=True):
		print '| {:>20} | {:>15} |'.format(s,comment_scores[s])
		print '------------------------------------------'

def print_subreddit_post_score():
	print '\n'
	print USER+' post score in subreddit :'
	print '------------------------------------------'
	print '| {:>20} | {:>15} |'.format("Subreddit", "Score")
	print '------------------------------------------'
	for s in sorted(post_scores, key=post_scores.get, reverse=True):
		print '| {:>20} | {:>15} |'.format(s,post_scores[s])
		print '------------------------------------------'

def print_time(start_time):
	print("--- %s seconds ---" % (time.time() - start_time))


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def subreddit_score(SUBREDDIT, SCORE, TYPE):
	if TYPE == 'comments':
		if SUBREDDIT in comment_scores:
			comment_scores[SUBREDDIT] = comment_scores[SUBREDDIT] + SCORE
		else:
			comment_scores[SUBREDDIT] = 1
	else:
		if SUBREDDIT in post_scores:
			post_scores[SUBREDDIT] = post_scores[SUBREDDIT] + SCORE
		else:
			post_scores[SUBREDDIT] = 1

def make_csv():
	with open('reddit.csv', 'wb') as csvfile:
	    csvwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
	    for subreddit in comment_scores:
	    	if subreddit in post_scores:
			    csvwriter.writerow([subreddit, comment_scores[subreddit], post_scores[subreddit]])

# Main Execution # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
if __name__ == '__main__':
	start_time = time.time()
	args = sys.argv[1:]
	while len(args) and args[0].startswith('-') and len(args[0]) > 1:
		arg = args.pop(0)
		if arg == '-c':
			CSV = True
		elif arg == '-h':
			usage(0)
		elif arg == '-n':
			NUMTOPBOT = int(args.pop(0))
		elif arg == '-p':
			PNG = True
		elif arg == '-s':
			SILENT = True
		elif arg == '-u':
			USER = args.pop(0)
		
		else:
			usage(1)

	# Parse through data:
	if SILENT:
		TYPE = 'comments'
		parse_user_history(TYPE)
		TYPE = 'submitted'
		parse_user_history(TYPE)
	else:
		print("Parsing through comments and posts...")
		TYPE = 'comments'
		parse_user_history(TYPE)
		TYPE = 'submitted'
		parse_user_history(TYPE)
		print("Printing results...")
		print_top_bot(NUMTOPBOT)
		print_interests()
		print_family()
		print_subreddit_comment_score()
		print_subreddit_post_score()

	# Generate CSV file
	if CSV:
		make_csv()

	if PNG:
		if CSV == False:
			make_csv()
		# os.system('sort -f reddit.csv |  | tee reddit.csv')
		os.system('./score.py > score.dat')
		os.system('gnuplot < score.plt > score.png')


	# Print Overview:
	print_top_bot(NUMTOPBOT)
	print_interests()
	print_family()
	print_time(start_time)
