#!/usr/bin/env python2.7
#
###
#   Title: pQueue.py
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


# Future # # # # # # # # # # # # # # # # # # #
# Handle Separate Queues for Comments and Posts
# 


# Imported Libraries
import collections
from heapq import heappush, heappop, nlargest, nsmallest
import os
import requests
import sys

# Object
myNode = collections.namedtuple('myNode', ['score', 'comment'])

# Define Variables:
STREAM 			= ''
COMMENTHEAP 	= []
NUMCOMMENTS 	= 10
NUMTOPBOTCOMM 	= 3
USER 			= 'madviet'

HEADERS  		= {'user-agent': 'reddit-{}'.format(os.environ['USER'])}

# Define Functions:
def usage(status):
	print '''Usage: {} -u USER
	-u USER	         The reddit user you wish to look up
	-tb NUM(TOP/BOT)  The number of top/bottom comment scores
	-n NUMCOMMENTS   The number of user comments to analyze'''.format(
		os.path.basename(sys.argv[0])
	)
	sys.exit(status)

# Function that gets the userscore
def get_score(comment_number=0):
	return url["data"]["children"][comment_number]["data"]["score"]

# Function that gets the comment
def get_comment(comment_number=0):
	return url["data"]["children"][comment_number]["data"]["body"]

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

	# Initialize variables for user data.
	web_address = 'https://www.reddit.com/u/'+USER+'/comments/.json'
	url = requests.get(web_address,headers=HEADERS).json()

	for comment in range(0, NUMCOMMENTS):			# Numbers from 0 to 9
		try:
			score = get_score(comment)
			comment = get_comment(comment)
			node = myNode(score = score, comment = comment)
			heappush(COMMENTHEAP, node)
		except IndexError,e:
			print "Error:", str(e)
			print "The user", USER, "does not have", NUMCOMMENTS, "comments."
			sys.exit(1)
	
	a = nlargest(NUMTOPBOTCOMM, enumerate(COMMENTHEAP), key=lambda x: x[1])
	print a

	print "a"

	b = nsmallest(NUMTOPBOTCOMM, enumerate(COMMENTHEAP), key=lambda x: x[1])
	print b

	# for comment in COMMENTHEAP:
	# 	print COMMENTHEAP.second

	# Print lowest and highest comments from the heap.
	# for i in range(0, NUMTOPBOTCOMM):
	# 	print COMMENTHEAP.pop()

	#for i in reversed(COMMENTHEAP)



