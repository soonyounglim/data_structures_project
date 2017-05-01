set terminal png
set grid
set key left
set style data histogram
set style histogram cluster gap 1
set style fill solid border
set boxwidth .95 relative
set ylabel "Score"
set xtics rotate
set xlabel "Subreddit"
set title "Comment Score Average vs. Subreddit"

plot	'comment_average.dat' using 2:xtic(1) title "Average"