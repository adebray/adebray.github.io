#!/usr/bin/env python3.4

# Arun Debray
# Started: 29 Jun 2014
# Updated: 10 Aug 2014

# The part of my project that makes pretty graphs.
# Uses matplotlib.

import argparse

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.axis as axis

# Setup: without arguments, makes all plots.
# With arguments, makes only the selected plots.
# Expand as necessary.
def handle_args():
	parser = argparse.ArgumentParser(description = 'generate plots from sleep data')
	# TODO: abstract these away into a function.
	parser.add_argument('--plot-times', dest = 'should_plot_times', action = 'store_true',
						default = None, help = 'create the times plot in plots/raw_times.pdf')
	parser.add_argument('--plot-probs', dest = 'should_plot_probs', action = 'store_true',
						default = None, help = 'create the probs. plot in plots/sleep_pobs.pdf')
	parser.add_argument('--plot-boxes', dest = 'should_plot_boxes', action = 'store_true',
						default = None, help = 'create boxplots of sleep by week. plot in *_box.pdf')
	args_dict = parser.parse_args()
	return [args_dict.should_plot_times,
		    args_dict.should_plot_probs,
			args_dict.should_plot_boxes]

# plot the times I slept and awoke
def plot_raw_times():
	print('Generating plot of times...')
	dbd = 735401 # offset of start date from 01-01-0001 UTC
	with open('raw_times.txt', 'r') as infile:

		time_data = [[float(s2) for s2 in s1.split('\t')] for s1 in infile]
		x = np.arange(dbd, dbd+len(time_data))
		
		_, ax = plt.subplots()
		fmt = dates.DateFormatter('%m/%d')
		ax.xaxis.set_major_formatter(fmt)

		ax.plot_date(x, [a[0] for a in time_data], fmt='bo', marker='x', label='slept', linestyle='-')
		ax.plot_date(x, [a[1] for a in time_data], color='r', marker='x', label='got up', linestyle='-')
	
		plt.legend(loc='center left')
		plt.title('Sleep Times')
		plt.ylabel('Time')

		plt.ylim(ymin = -3, ymax = 12) # may need to change this once the school year starts.
		plt.yticks(np.arange(-3,13), [str(n % 24) + ":00" for n in range(-3,13)])
		plt.grid(b='on', which='major', axis='y', linestyle=':')

		# may change to eps for file-size stuff later.
		plt.savefig('plots/raw_times.pdf', format='pdf')

# plot the probability that I am awake at a given time
# this would be interesting in the last 7 or 30 days.
def plot_raw_probs():
	print('Generating plot of probabilities...')
	with open('raw_probs.txt', 'r') as infile:
		probs_vector = [float(line) for line in infile]
		x = np.arange(0.0, 24.1, 0.1)
		probs_vector.append(probs_vector[0])

		plt.plot(x, probs_vector, color = '#D20DFF', linewidth = 2)
		plt.fill_between(x, probs_vector, alpha = 0.5, color = '#EFC0FA')

		plt.xlim(xmin = 0, xmax = 24)
		plt.xticks(np.arange(0, 24.1, 4), ['%d:00' % n for n in [0, 4, 8, 12, 16, 20, 24]])
		plt.xlabel('Time of day')

		plt.ylim(ymin = 0, ymax = 1.005) # dat font doe
		plt.yticks(np.arange(0.0, 1.01, 0.1), ['%.1f' % n for n in np.arange(0.0, 1.01, 0.1)])
		plt.ylabel('Probability I am asleep')

		plt.title('Distribution of sleep times')

		# This only comes up if plot_raw_times is suppressed
		# Still generates a warning... hopefully, I'll fix that.
		if plt.legend() is not None:
			plt.legend().set_visible(False)

		plt.savefig('plots/sleep_probs.pdf', format='pdf')


def get_sleep_times():
	with open('raw_times.txt', 'r') as f:
		return [float(line.split()[0]) for line in f]

def get_wake_times():
	with open('raw_times.txt', 'r') as f:
		return [float(line.split()[1]) for line in f]

# cycles the list so that Monday starts the awake work week, and
# Sunday the asleep work week.
# basically, restarts the cycle with arr[offset]
def rearrange(arr, offset):
	return arr[offset:] + arr[:offset]

# probably will add an optional colorscheme argument...
# and prettfiy the fonts on the y-axis.

# offset is how different the second plot is.
def boxplot_data(fn, fname, ymin, ymax, offset = 0, cmap = 'muted'):
	# this is a little hacky: I just wanted to combine the two Python programs I had, but
	# without messing with the styles. I can unify/prettify everything another time.
	import seaborn as sns

	times = fn()
	# sort by day of the week
	organized_data = [[x for j, x in enumerate(times) if j % 7 == (i + 5) % 7] for i in range(7)]

	# and then the plotting

	sns.set(style = 'ticks')
	f, ax = plt.subplots()
#   sns.offset_spines()
	sns.boxplot(organized_data, fliersize = 6, names = rearrange(['Sunday', 'Monday', 'Tuesday',
			'Wednesday', 'Thursday', 'Friday', 'Saturday'], offset), color = cmap)
	plt.ylim(ymin, ymax)
	plt.yticks(np.arange(ymin, ymax + 1), ['%d:00' % (n % 24) for n in np.arange(ymin, ymax + 1)])
	sns.despine(trim=True)

	plt.savefig('plots/' + fname)

def plot_boxes():
	print('Generating weekly boxplot breakdown...')
	boxplot_data(get_sleep_times, 'asleep_box.pdf', ymin = -2, ymax = 3, cmap = 'cool')
	boxplot_data(get_wake_times, 'awake_box.pdf', ymin = 6, ymax = 11, offset = 1, cmap = 'hot')

# This isn't yet part of the program, but is experimental testing cool stuff. hehehehe
# I promise there's no evil plotting going on here. No sir.
def window_plotting():
	print('Generating moving averags plot') # will be more general later
	with open('weekly_moving_avgs.txt') as f:
		data = [float(line) for line in f]

	dbd = 735401
	_, ax = plt.subplots()
	fmt = dates.DateFormatter('%m/%d')
	ax.xaxis.set_major_formatter(fmt)

	xs = np.arange(dbd, dbd+len(data))
	# note to self: make this look pretty someday.
	ax.plot_date(xs, data, color='r', marker='x', linestyle='-')
	plt.savefig('plots/weekly_moving_averages.pdf')

# A histogram of when I fell asleep.
# Not currently being used. I should do something with it.
def asleep_histogram():
	with open('raw_times.txt', 'r') as infile:
		asleep_data = [float(line.split('\t')[0]) for line in infile]

		plt.hist(asleep_data, color='#3FA5FF')

		plt.xlim(xmin = -2, xmax = 3) # will almost certainly need to change. q_q
		plt.xticks(np.arange(-2, 3), ['%d:00' % (n % 24) for n in np.arange(22, 28)])

		plt.savefig('plots/asleep_histogram.pdf', format='pdf')

def main():
	#window_plotting() # TODO
	#return

	flags = handle_args()
	# update as necessary
	to_plot = [plot_raw_times, plot_raw_probs, plot_boxes]
	if any(flags):
		_ = [plotfn() for flag, plotfn in zip(flags, to_plot) if flag]
	else: # no flags specified, do everything
		_ = [plotfn() for plotfn in to_plot]
#	asleep_histogram()

if __name__ == '__main__':
	main()
