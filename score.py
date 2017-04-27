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

PATH = './reddit.csv'

if __name__ == '__main__':
	# Open and read csv file
	with open(PATH, 'r') as f:
		for line in f:
			print line,

	# Close csv file
	f.close()



'''
# Set url variable.
URL=https://www3.nd.edu/~pbui/teaching/cse.20289.sp17/static/csv/demographics.csv

count_gender() {
    column="$((($1 - 2013) * 2 + 1))"
    gender=$2

    # Count gender in the column.
    curl -s $URL | cut -d , -f $column | grep $gender | wc -l

}

# Output.
for year in $(seq 2013 2019); do
    echo $year $(count_gender $year F) $(count_gender $year M)
done

x   y
2013 14 49
2014 12 44
2015 16 58
2016 19 60
2017 26 65
2018 36 90
2019 51 97
'''