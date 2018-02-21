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

# returns full path to the git repo
def path_to_repo() -> str:
	return capture_output('git', 'rev-parse', '--show-toplevel').decode('UTF-8')[:-1]

# equivalent to the shell command `git reflog | head -2`, which lists the two most recent hashes
# (which we are assuming (NOTE) are before and after the most recent git pull)
def last_two_hashes() -> (str, str):
	raw_info = capture_output('git', 'reflog').decode('UTF-8').splitlines()[:2]
	return map(lambda s: s.split()[0], raw_info)

# return the list of files that have changed between the two pulls given by the last two hashes
def files_to_check() -> [str]:
	hash1, hash2 = last_two_hashes()
	files = capture_output('git', 'diff', '--name-only', hash1, hash2).decode('UTF-8').splitlines()
	return files

# return date of last update given file
def last_update(filename) -> str:
	raw_info = capture_output('git', '--no-pager', 'log', '-1', '--pretty=format:"%ad"',
		filename).decode('UTF-8 ')
	if raw_info == '':
		return datetime.datetime.now().strftime('%b %d, %y')
	return datetime.datetime.strptime(raw_info, '"%a %b %d %X %Y %z"').strftime('%B %d, %Y')

# recursively obtain all files, ignoring hidden directories and symlinks
# def all_files() -> [str]:
# 	for root, dirs, files in os.walk('.', topdown=True):
# 		dirs[:] = [d for d in dirs if d not in ('.git', 'SURIM', 'other')]
# 		for filename in files:
# 			yield '%s/%s' % (root, filename)

# dictionary of filename -> when last updated
def changed_files_info() -> dict:
	# filename is relative to the base of the git repo
	# so we prepend the full path to the git repo so that last_update finds the file
	git_root = path_to_repo() + '/'
	return {filename: last_update(git_root + filename) for filename in files_to_check()}

def main():
	with open('.git/update_info.js', 'w') as infile:
		infile.write('var all_files_info = %s;' % changed_files_info())

if __name__ == '__main__':
	main()
