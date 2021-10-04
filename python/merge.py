#!/usr/bin/env python3

# Arun Debray
# 4 March 2017, updated 4 October 2021

# usage:
# ./merge.py
#	Updates only the files that have changed in the last two commits
# ./merge-py -all
#	Updates all files. (This takes longer, which is why it's not the default.)

# git hook to produce a dictionary of when each file was last updated.

import datetime
import json
import os
import subprocess
import sys

# this is a hack that allows me to avoid properly parsing update_info.js
JS_BEGIN_LENGTH = len('var all_files_info = ')
DIRS_TO_IGNORE = ('.git', 'SURIM', 'other')

# I wish I didn't have to encode this as a global, but in the current usage I never need to run this
# anywhere except in this directory
WORKING_DIR = '/export/userswww/adebray/WWW'
#WORKING_DIR = '/home/a.debray/public_html'

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
def recently_changed_files(_) -> [str]:
	hash1, hash2 = last_two_hashes()
	# this names the files relative to the git root directory
	files = capture_output('git', 'diff', '--name-only', '--diff-filter=d', hash1, hash2).decode('UTF-8').splitlines()
	# but we want the absolute file path, so prepend WORKING_DIR
	return map(lambda x: WORKING_DIR + '/' + x, files)

# return date of last update given file
def last_update(filename: str) -> str:
	raw_info = capture_output('git', '--no-pager', 'log', '-1', '--pretty=format:"%ad"',
		filename).decode('UTF-8 ')
	print(filename, raw_info)
	if raw_info == '':
		return datetime.datetime.now().strftime('%b %d, %y')
	return datetime.datetime.strptime(raw_info, '"%a %b %d %X %Y %z"').strftime('%B %d, %Y')

# recursively obtain all files, ignoring hidden directories and symlinks
def all_files(git_root) -> [str]:
	for root, dirs, files in os.walk(WORKING_DIR, topdown=True):
		dirs[:] = [d for d in dirs if d not in DIRS_TO_IGNORE]
		for filename in files:
			#print(root, filename)
			yield '%s/%s' % (root, filename)

# dictionary of filename -> when last updated
def changed_files_info(git_root: str, old_info: dict, files_to_check) -> dict:
	# filename is relative to the base of the git repo
	# so we prepend the full path to the git repo so that last_update finds the file
	for filename in files_to_check(git_root):
		#full_file_path = git_root + '/' + filename
		# the js references just the filename (no basename)
		old_info[filename] = last_update(filename)
	return old_info

# Returns false on ./merge.py and true on ./merge.py -all
def run_on_all_files() -> bool:
	return len(sys.argv) > 1 and sys.argv[1] == '-all'

def main():
	# If -all was specified, we'll check on all files; otherwise only recently changed ones.
	# This line tells us which method to call to come up with the list of files
	files_to_check = all_files if run_on_all_files() else recently_changed_files
		
	# this allows us to run merge.py from anywhere in the repo
	git_root = path_to_repo()
	js_info_file = git_root + '/' + '.git/update_info.js'
	old_info = dict()
	# fixing a bug that I had
	try:
		with open(js_info_file, 'r') as infile:
			# the file begins with 'var all_files_info = ' which we don't want to parse.
			# this has length JS_BEGIN_LENGTH, so we just skip it
			old_info = loads_with_single_quotes(infile.read()[JS_BEGIN_LENGTH:-1])
	# sometimes this fails update_info.js is gone
	except FileNotFoundError:
		pass
	# or maybe update_info.js exists and is empty
	except json.decoder.JSONDecodeError:
		pass
	with open(js_info_file, 'w') as infile:
		infile.write('var all_files_info = %s;' % changed_files_info(git_root, old_info, files_to_check))

if __name__ == '__main__':
	main()
