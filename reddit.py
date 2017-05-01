#!/usr/bin/env python2.7
#  reddit.py  :  Parses a redditor's history to pull certain attributes, (un)popular comments/posts, and more...
#  Authors    :  Soonyoung Lim, Anthony Luc, and Donald Luc
#  Data Structures Final Project

# Import Modules:
import collections
import csv
from heapq import heappush, heappop, nlargest, nsmallest
import os
import sys
import re
import requests
import time

# Define Variables:
USER              = 'spez'
POSTS_PER_PAGE    = 25
HEADERS           = {'user-agent': 'reddit-{}'.format(os.environ['USER'])}
TYPE              = ''
CSV               = False
PNG               = False
SILENT            = False

# Heap Variables
NUMTOPBOT 	      = 3      # Total number to print
COMMENTHEAP 	  = []     # Heap with myPair tuples of score and body
POSTHEAP 		  = []     # Heap with myPair tuples of score and body
myPair            = collections.namedtuple('myPair', ['score', 'body'])    # Define Object for use in the heap

# Dictionaries
interests         = {}     # Key: Subreddit       Value: Total occurrence
comment_scores    = {}     # Key: Subreddit       Value: Score
post_scores       = {}     # Key: Subreddit       Value: Score

# Lists
male_list         = []
female_list       = []
age_list          = []
family_list       = []

# Regular Expressions
regex_male        = r'\b(I am|I am a|as a) (man|boy|guy|male)\b'
regex_female      = r'\b(I am|I am a|as a) (woman|girl|lady|female)\b'
regex_age         = r'\b(I am|I am a|I\'m|I\'m a).*[0-9]+.(years|year|yrs|yr).old\b'
regex_family      = r'\b(I have|I have a|my|our).*(older|younger|step|twin)?.*(brother|bro|sister|sis|dad|daddy|papa|father|mom|mommy|mama|mother|cousin|uncle|aunt)\b'

# Define Functions:
def usage(status):
	print '''Usage: {} ...
	-c               Create a csv file
	-n NUMBER        The number of top and bottom comment/post scores
	-s SILENT        Silence output
	-p               Generate a barchart of data in a png
	-u USER	         The reddit user you wish to look up'''.format(
		os.path.basename(sys.argv[0])
	)
	sys.exit(status)

# Parsing functions # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def parse_user_history(TYPE):
	# Check if user exists by seeing if initial page is valid.
	try:
		next_page = get_initial_page(TYPE)
	except KeyError:
		print "Error: user {} does not exist.".format(USER)
		sys.exit(1)

	# Continue parsing through pages...
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
			link_url = get_data(URL_JSON, i, 'link_url')
			store_heap(score, body, TYPE)
			subreddit_score(subreddit, score, TYPE)
			find_regex(body, link_url)

		# Get metadata for post/submitted.
		else:
			post_title = get_data(URL_JSON, i, 'title')
			self_post = get_data(URL_JSON, i, 'is_self')

			if self_post:
				body = get_data(URL_JSON, i, 'selftext')
				url = URL_JSON['data']['children'][i]['data']['url']
				find_regex(body, url)

			store_heap(score, post_title, TYPE)
			subreddit_score(subreddit, score, TYPE)

		# Update user's interests counter
		if subreddit in interests:
			interests[subreddit] = interests[subreddit] + 1
		else:
			interests[subreddit] = 1

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

# Utility functions # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def find_regex(BODY, URL):
	# Find Gender.
	found_male = re.search(regex_male, BODY)
	if found_male:
		male_list.append(found_male.group())
		male_list.append(URL)
	found_female = re.search(regex_female, BODY)
	if found_female:
		female_list.append(found_female.group())
		female_list.append(URL)

	# Find Age.
	found_age = re.search(regex_age, BODY)
	if found_age:
		age_list.append(found_age.group())
		age_list.append(URL)

	# Find Family.
	found_family = re.search(regex_family, BODY)
	if found_family:
		family_list.append(found_family.group())
		family_list.append(URL)



def make_csv():
	with open('reddit.csv', 'wb') as csvfile:
	    csvwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
	    for subreddit in comment_scores:
	    	if subreddit in post_scores:
			    csvwriter.writerow([subreddit, comment_scores[subreddit], post_scores[subreddit]])

def store_heap(SCORE, BODY, TYPE):
	node = myPair(score = SCORE, body = BODY)
	if TYPE == 'comments':
		heappush(COMMENTHEAP, node)
	else: # submitted
		heappush(POSTHEAP, node)

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

# Print Functions # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def print_top_bot(NUMTOPBOT=NUMTOPBOT):
	print "Top", NUMTOPBOT, "Comments:"
	a = nlargest(NUMTOPBOT, enumerate(COMMENTHEAP), key=lambda x: x[1])
	print_heap(a, 'comments')

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

def print_subreddit_comment_score():
	print '\n'
	print USER+' comment score in subreddit :'
	print '------------------------------------------'
	print '| {:>20} | {:>15} |'.format("Subreddit", "Score")
	print '------------------------------------------'
	for s in sorted(comment_scores, key=comment_scores.get, reverse=True):
		if comment_scores[s] != 1:  # Ignore insignificant comment scores
			print '| {:>20} | {:>15} |'.format(s,comment_scores[s])
			print '------------------------------------------'

def print_subreddit_post_score():
	print '\n'
	print USER+' post score in subreddit :'
	print '------------------------------------------'
	print '| {:>20} | {:>15} |'.format("Subreddit", "Score")
	print '------------------------------------------'
	for s in sorted(post_scores, key=post_scores.get, reverse=True):
		if post_scores[s] != 1:     # Ignore insignificant post scores
			print '| {:>20} | {:>15} |'.format(s,post_scores[s])
			print '------------------------------------------'

def print_interests():
	print '\n'
	print USER+'\'s top interests are:'
	print '------------------------------------------'
	print '| {:>20} | {:>15} |'.format("interest","# of occurences")
	print '------------------------------------------'
	for i in sorted(interests, key=interests.get, reverse=True)[:10]:
		print '| {:>20} | {:>15} |'.format(i,interests[i])
		print '------------------------------------------'

def print_regex():
	print '\n'
	print USER+' is a:'
	print '------------------------------------------'
	count = 0
	if male_list:
		for m in male_list:
			print m

	count = 0
	if female_list:
		for f in female_list:
			print f

	count = 0
	if age_list:
		for a in age_list:
			print a

	count = 0
	if not (male_list or female_list or age_list):
		print 'Cannot determine gender and age'

	print '\n'
	print USER+' has family members:'
	print '------------------------------------------'
	count = 0
	if family_list:
		for fam in family_list:
			count = count + 1
			print fam
			if (count % 2) == 0:
				print '\n'
	else:
		print 'Cannot determine family'

def print_time(start_time):
	print("--- %s seconds ---" % (time.time() - start_time))


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

	# Parse through reddit JSON data.
	if SILENT:
		TYPE = 'comments'
		parse_user_history(TYPE)
		TYPE = 'submitted'
		parse_user_history(TYPE)
	else:
		# Print to stdout.
		print("Parsing through {} comments and posts...".format(USER + '\'s'))
		TYPE = 'comments'
		parse_user_history(TYPE)
		TYPE = 'submitted'
		parse_user_history(TYPE)
		print("Printing results...")
		print_top_bot(NUMTOPBOT)
		print_subreddit_comment_score()
		print_subreddit_post_score()
		print_interests()
		print_regex()
		print_time(start_time)

	# Generate CSV file.
	if CSV:
		make_csv()

	# Generate PNG
	if PNG:
		if CSV == False:
			make_csv()
		os.system('./score.py > score_temp.dat')       # TODO: new plt file and new png names
		os.system('sort -f score_temp.dat > score.dat')
		os.system('gnuplot < score.plt > {}.png'.format(USER))
		os.system('rm score_temp.dat score.dat')
		if CSV == False:
			os.system('rm reddit.csv')

