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
#import io
import os
import requests
import sys
import heapq

# Define Variables:
STREAM 		= ''
MYHEAP 		= heapq
SCOREARR 	= []

HEADERS  	= {'user-agent': 'reddit-{}'.format(os.environ['USER'])}
USER 		= 'madviet'

# Define Functions:
def usage(status):
	print '''Usage: {} -u USER
	-u USER		The reddit user you wish to look up'''.format(
		os.path.basename(sys.argv[0])
	)
	sys.exit(status)

# Function that gets the userscore
def get_score(comment_number=0):
	return url["data"]["children"][comment_number]["data"]["score"]

# Main Execution:
if __name__ == '__main__':
	args = sys.argv[1:]
	while len(args) and args[0].startswith('-') and len(args[0]) > 1:
		arg = args.pop(0)
		if arg == '-h':
			usage(0)
		elif arg == '-u':
			USER = args.pop(0)
		else:
			usage(1)

	# Initialize variables for user data.
	web_address = 'https://www.reddit.com/u/'+USER+'/comments/.json'
	url = requests.get(web_address,headers=HEADERS).json()

	for comment in range(0,10):			# Numbers from 0 to 9
		try:
			score = get_score(comment)
			SCOREARR.append(score)
			#MYPQ.put(score)
		except:
			break
	
	print url["data"]["children"][1]["data"]["link_id"]
	
	print SCOREARR

	# Print highest and lowest comments from the heap.
	'''
	try
	except(IndexError):
	'''





# Note: dir(myPQ)
'''
['__doc__',
 '__init__',
 '__module__',
 '_get',
 '_init',
 '_put',
 '_qsize',
 'empty',
 'full',
 'get',
 'get_nowait',
 'join',
 'put',
 'put_nowait',
 'qsize',
 'task_done']
'''
