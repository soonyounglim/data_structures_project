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
import io
import os
import sys
from Queue import PriorityQueue

# Global Variables
STREAM 		= ''
myPQ 		= PriorityQueue

# Functions
def usage(exit_code=0):
	print '''Usage: {} [-s stream]
	-s stream   Input stream'''.format(os.path.basename(sys.argv[0]))
	sys.exit(exit_code)

if __name__ == '__main__':
	# Parse command line arguments
	args = sys.argv[1:]
	while len(args) and args[0].startswith('-') and len(args[0]) > 1:
		arg = args.pop(0)
		if arg == '-h':
			usage(0)
		elif arg == '-p':
			PREFIX = args.pop(0)			# Get the prefix
		elif arg == '-s':
			HASHES = args.pop(0)			# Get the path of the hashs file
		else:
			usage(1)

	print 'a'
	print dir(myPQ)

	# Print contents of priority_queue

	# Think about how to store for memory
	




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
