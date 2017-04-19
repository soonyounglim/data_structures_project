#!/usr/bin/env python2.7
#
###
#   Title: heap.py
#   Author: Anthony Luc
#   Date: April 2, 2017
#   Course: Data Structures 2017
#   Assignment: Final Project
#
#   About: Practicing using the priority queue in python
#
#	Source: https://docs.python.org/2/library/queue.html
#			http://stackoverflow.com/questions/9289614/how-to-put-items-into-priority-queues
#
###

# Imported Libraries
import collections
from heapq import heappush, heappop, nlargest, nsmallest
import os
import requests
import sys

# Object
myPair = collections.namedtuple('myPair', ['score', 'body'])

# Define Variables:
STREAM 			= ''
COMMENTHEAP 	= []
NUMCOMMENTS 	= 10
NUMTOPBOTCOMM 	= 3
POSTHEAP 		= []
NUMPOSTS 		= 10
NUMTOPBOTPOST	= 3
USER 			= 'madviet'

HEADERS  		= {'user-agent': 'reddit-{}'.format(os.environ['USER'])}

# Define Functions:
def usage(status):
	print '''Usage: {} -u USER
	-u USER	          The reddit user you wish to look up
	-tb NUM(TOP/BOT)  The number of top/bottom comment scores
	-n NUMCOMMENTS    The number of user comments to analyze'''.format(
		os.path.basename(sys.argv[0])
	)
	sys.exit(status)

# Function that gets the userscore
def get_score(obj_number=0):
	return url["data"]["children"][obj_number]["data"]["score"]

# Function that gets the comment body
def get_comment(comment_number=0):
	return url["data"]["children"][comment_number]["data"]["body"]

# Function that gets the post title
def get_post(post_number=0):
	return url["data"]["children"][post_number]["data"]["title"]

# Function that prints the heap nicely
def print_heap(heap):
	for k,v in enumerate(heap):
		print "#", k, "\tScore:", v[1][0], "\tBody:", v[1][1], "\n"

# Main Execution:
if __name__ == '__main__':
	args = sys.argv[1:]
	while len(args) and args[0].startswith('-') and len(args[0]) > 1:
		arg = args.pop(0)
		if arg == '-h':
			usage(0)
		elif arg == '-u':
			USER = args.pop(0)
		elif arg == '-n':
			NUMCOMMENTS = int(args.pop(0))
		elif arg == '-tb':
			NUMTOPBOTCOMM = int(args.pop(0))
		else:
			usage(1)

	# Initialize variables for user data for comments.
	web_address = 'https://www.reddit.com/u/'+USER+'/comments/.json'
	url = requests.get(web_address,headers=HEADERS).json()

	for comment in range(0, NUMCOMMENTS):
		try:
			score = get_score(comment)
			comment = get_comment(comment)
			node = myPair(score = score, body = comment)
			heappush(COMMENTHEAP, node)
		except IndexError,e:
			print "Error:", str(e)
			print "The user", USER, "does not have", NUMCOMMENTS, "comments."
			sys.exit(1)
	
	a = nlargest(NUMTOPBOTCOMM, enumerate(COMMENTHEAP), key=lambda x: x[1])
	print_heap(a)

	b = nsmallest(NUMTOPBOTCOMM, enumerate(COMMENTHEAP), key=lambda x: x[1])
	print_heap(b)

	# Update variables for user data for posts.
	web_address = 'https://www.reddit.com/u/'+USER+'/submitted/.json'
	url = requests.get(web_address,headers=HEADERS).json()

	for post in range(0, NUMPOSTS):
		try:
			score = get_score(post)
			post = get_post(post)
			node = myPair(score = score, body = post)
			heappush(POSTHEAP, node)
		except IndexError,e:
			print "Error:", str(e)
			print "The user", USER, "does not have", NUMPOSTS, "posts."
			sys.exit(1)

	a = nlargest(NUMTOPBOTPOST, enumerate(POSTHEAP), key=lambda x: x[1])
	print_heap(a)

	b = nsmallest(NUMTOPBOTPOST, enumerate(POSTHEAP), key=lambda x: x[1])
	print_heap(b)

	# for comment in COMMENTHEAP:
	# 	print COMMENTHEAP.second

	# Print lowest and highest comments from the heap.
	# for i in range(0, NUMTOPBOTCOMM):
	# 	print COMMENTHEAP.pop()

	#for i in reversed(COMMENTHEAP)



