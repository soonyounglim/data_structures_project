#!/usr/bin/env python2.7
#
###
#   Title: score.py
#   Author: Anthony Luc
#   Date: April 29, 2017
#   Course: Data Structures
#   Assignment: Final Project
#
#   About: Extracts score corresponding to subreddit from the csv file
#
#   Usage: score.py
#
###

FILE        = 'reddit.csv'

if __name__ == '__main__':
	# Open and read csv file
	with open(FILE, 'r') as f:
		for line in f:
			line = line.replace(",", " ")
			print line,

	# Close csv file
	f.close()
