set terminal png
set grid
set key right
set style data histogram
set style histogram cluster gap 1
set style fill solid border
set boxwidth .95 relative
set ylabel "Score"
set xlabel "Subreddit"

plot	'score.dat' using 2:xtic(1) title "Comments",\
	'score.dat' using 3 title "Posts"