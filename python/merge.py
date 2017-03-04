#!/usr/bin/env python3

# Arun Debray
# 4 March 2017

# git hook to produce a dictionary of when each file was last updated.

import datetime
import subprocess
import os

# execute command, return stdout
def capture_output(*args) -> str:
	return subprocess.check_output(args)

# get 6-digit hash of latest tag
# def latest_tag() -> str:
#	return capture_output('git', 'describe', '--tags', '--always', '--dirty="-*"')

# return date of last update given file
def last_update(filename: str) -> str:
	raw_info = capture_output('git', '--no-pager', 'log', '-1', '--pretty=format:"%ad"',
		filename).decode('UTF-8 ')
	print(filename, raw_info)
	if raw_info == '':
		return datetime.datetime.now().strftime('%b %d, %y')
	return datetime.datetime.strptime(raw_info, '"%a %b %d %X %Y %z"').strftime('%B %d, %Y')


# recursively obtain all files, ignoring hidden directories and symlinks
def all_files() -> [str]:
	for root, dirs, files in os.walk('.', topdown=True):
		dirs[:] = [d for d in dirs if d not in ('.git', 'SURIM', 'other')]
		for filename in files:
			yield '%s/%s' % (root, filename)

# dictionary of filename -> when last updated
def all_files_info() -> dict:
	return {filename: last_update(filename) for filename in all_files()}

def main():
	with open('.git/update_info.js', 'w') as infile:
		infile.write('var all_files_info = %s;' % all_files_info())

if __name__ == '__main__':
	main()
