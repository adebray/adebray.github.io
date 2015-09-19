#!/usr/bin/env python2.7

# Arun Debray, 9 February 2014
# Using matplotlib to deal with ping data from axess.stanford.edu on the
# night that course enrollment opens.

# This program lives at https://adebray.github.io/python/pingTimeGraph.py,
# and the data I ran it on is at https://adebray.github.io/python/axess_data.txt.

# Usage: ./pingTimeGraph.py datafile

#inAxessible

import sys
import numpy as np
import matplotlib.pyplot as plt

# Convert hours, minutes, seconds to an integer. Seconds implicit: pings were done every 15s.
# Note: 10pm to 2am represented as 10 to 14, since this was done over midnight.
# I could do this as time series but don't care enough
def step_in_time(ping_data):
	clock_times = []
	# artificially adding minutes.
	minute_times = 0
	last_minute = 0
	for i in range(len(ping_data)):
		hours, minutes, _ = ping_data[i]
		if hours < 6:
			hours += 12
		else:
			hours -= 12
		if minutes == last_minute:
			minute_times += 1
		else:
			minute_times = 0
			last_minute = minutes
		seconds = 15 * minute_times
		clock_times.append(hours + minutes / 60.0 + seconds / 3600.0)
	return clock_times

# Calculates average centered around a ping time. Might make for a better plot.
#def smooth_ping_times(ping_times):
#	smoothed_times = []
#	smoothness = 3
#	for i in range(len(ping_times)):
#		neighbors = ping_times[max(0, i - smoothness): min(len(ping_times), i + smoothness + 1)]
#		smoothed_times.append(sum(neighbors)/len(neighbors))
#	return smoothed_times

# First, I need to extract the information. This might be janky.
# Returns a tuple with the following data:
#	(hour, minute, ping_time in ms)
#	If ping_time is negative, then there was a request timeout.
def ping_time_parse(datastring):
	times = datastring[0:5].split(':')
	if (len(times) > 3 or (len(times) == 3 and times[2] != '')):
		sys.stderr.write('Could not parse the time on string \'%s\'.' % datastring)
		return
	hours = int(times[0])
	minutes = int(times[1])
	if 'Request timeout' in datastring:
		return (hours, minutes, -1)
	ping_time_index = datastring.find('time=')
	if ping_time_index == -1:
		sys.stderr.write('Could not parse the time on string \'%s\'.' % datastring)
		return
	ping_time = float(datastring[ping_time_index + 5: -4])
	return (hours, minutes, ping_time)

# One function for all of the little fiddly things I do in order
# to make the graph look good.
def make_plot(clock_times, ping_times):
	plt.plot(clock_times, ping_times)
	plt.xlim(11, 14)
	plt.xticks(np.arange(11, 14.01, 0.5), ('11:00', '11:30', '12:00', '12:30', '1:00', '1:30', '2:00'))
	plt.ylabel('Ping time (ms)')
#	plt.show()
	plt.savefig('axess_graph2.png')

# Returns a tuple (clock_times, ping_times) of NumPy arrays of data.
# Factored out so I can fiddle with, for example, request timeouts.
def obtain_data(filename):
	with open(filename, 'r') as infile:
		parse_tuples = [ping_time_parse(line) for line in infile]
		# Right now, I'm ignoring request timeouts
		clock_times = step_in_time([tup for tup in parse_tuples if tup[2] > 0])
#		ping_times = smooth_ping_times([tup[2] for tup in parse_tuples if tup[2] > 0])
		ping_times = [tup[2] for tup in parse_tuples if tup[2] > 0]
		return (clock_times, ping_times)

def main():
	if len(sys.argv) < 2:
		print 'Usage: ./pingTimeGraph.py datafile.'
		print('No filename was specified.')
		exit()
	clock_times, ping_times = obtain_data(sys.argv[1])
	make_plot(clock_times, ping_times)

if __name__ == '__main__':
	main()
