# Project Name  :  Reddit
    Developers   :  Soonyoung Lim, Anthony Luc, and Donald Luc
    Course       :  Data Structures Project Spring 2017 
    Description  :  A Python script that parses a reddit account's comments and posts.
&nbsp;
&nbsp;
## General Idea
        Reddit is a network of communities where people can become connected
    via similar interests and participate in discussion. In order to
    participate in this network, a person must create a reddit account in
    order to comment and/or post content. There is a general anonymity
    attached to a redditor's online persona, but at times that redditor may
    leak some important details about themselves.
        Our reddit.py not only gives a general karma overview of any given
    redditor, but it also searches through all of the user's comments and
    posts to find 'leaked' attributes of that person such as gender, age, and
    any particular family members.
&nbsp;
&nbsp;
## Usage
```console
$ ./reddit.py -h
Usage: reddit.py...
    -c              Create a csv file
    -n NUMBER       The number of top and bottom comment/post scores
    -s SILENT       Silence output
    -p              Generate a barchart of data in a png
    -u USER         The reddit user you wish to look up
```
&nbsp;
&nbsp;
## Data Structures Implemented
    1. Dictionaries  :  Has the syntax of { key=subreddit, value=score }.
    2. Heaps  :  Ordered by comment/post score that displays the contents of -n comments/posts.
    3. Lists  :  Stores comments/posts that were successfully found via re.search().
&nbsp;
&nbsp;
## Visuals
    Print Out To The Console
    Top comments/posts, the total score of user activity in a particular
    subreddit, general frequency of user activity in a particular subreddit,
    and a the list of user attributes that compromises the user's anonymity.
    
    Created .png Files Via Gnuplot
    Post Score vs. Subreddit, Post Occurrence vs. Subreddit, and Post Average
    Score vs. Subreddit.