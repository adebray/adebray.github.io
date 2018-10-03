#!/usr/bin/env python3

# Arun Debray
# 4 March 2017

# git hook to produce a dictionary of when each file was last updated.

import datetime
import json
import os
import subprocess

# this is a hack that allows me to avoid properly parsing undate_info.js
JS_BEGIN_LENGTH = len('var all_files_info = ')

# since single quotes are not valid JSON, this just changes them to double quotes
# before calling json.loads
def loads_with_single_quotes(s: str):
	s = s.replace('\'', '"')
	return json.loads(s)

# execute command, return stdout
def capture_output(*args) -> str:
	return subprocess.check_output(args)

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
	files = capture_output('git', 'diff', '--name-only', '--diff-filter=d', hash1, hash2).decode('UTF-8').splitlines()
	return files

# return date of last update given file
def last_update(filename) -> str:
	raw_info = capture_output('git', '--no-pager', 'log', '-1', '--pretty=format:"%ad"',
		filename).decode('UTF-8 ')
	print(filename, raw_info)
	if raw_info == '':
		return datetime.datetime.now().strftime('%b %d, %y')
	return datetime.datetime.strptime(raw_info, '"%a %b %d %X %Y %z"').strftime('%B %d, %Y')

# recursively obtain all files, ignoring hidden directories and symlinks
#def all_files(git_root) -> [str]:
# 	for root, dirs, files in os.walk(git_root, topdown=True):
# 		dirs[:] = [d for d in dirs if d not in ('.git', 'SURIM', 'other')]
# 		for filename in files:
# 			print(root, filename)
# 			yield '%s/%s' % (root, filename)

# dictionary of filename -> when last updated
def changed_files_info(git_root: str, old_info) -> dict:
	# filename is relative to the base of the git repo
	# so we prepend the full path to the git repo so that last_update finds the file
	for filename in files_to_check():
		full_file_path = git_root + '/' + filename
		# the js references just the filename (no basename)
		old_info[full_file_path] = last_update(full_file_path)
	return old_info

def main():
	# this allows us to run merge.py from anywhere in the repo
	git_root = path_to_repo()
	js_info_file = git_root + '/' + '.git/update_info.js'
	old_info = dict()
	with open(js_info_file, 'r') as infile:
		# the file begins with 'var all_files_info = ' which we don't want to parse.
		# this has length JS_BEGIN_LENGTH, so we just skip it
		old_info = loads_with_single_quotes(infile.read()[JS_BEGIN_LENGTH:-1])
	with open(js_info_file, 'w') as infile:
		infile.write('var all_files_info = %s;' % changed_files_info(git_root, old_info))

if __name__ == '__main__':
	main()
