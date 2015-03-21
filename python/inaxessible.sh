#!/bin/bash

# Arun Debray, 8 February 2014

# Let's see what happens to ping times for Axess... heh
# Usage: ./inaxessible filename.txt

# Spits out the ping times to stdout, but also to a file so
# I can make a graph later.

if [ $# -lt 1 ]; then
	echo Usage: ./inaxessible filename.txt.
	exit
fi

while true
do
	echo -n $(date +%k:%M:%S)": " | tee -a $1
	ping -c 1 axess.stanford.edu | sed -n 2p | tee -a $1
	# Six times a minute ought to give me an idea.
	sleep 10
done

#inaxessible
