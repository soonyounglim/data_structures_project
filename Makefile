# Adapted from Reading04 in Sys Program's class
# Anthony Luc

all:	score.png

score.dat:	score.py
	./score.py > score.dat

score.png:	score.plt score.dat
	gnuplot < score.plt > score.png

clean:
	rm -f score.png score.dat
