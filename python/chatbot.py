#!/usr/bin/env python3.2

# A totally convincing AI chatbot meant to emulate Matt Staib.
# Arun Debray, 27 November 2013

import random
import subprocess

def reaction(s):
	response_list = ['IOWA!',
					 'WHOA IOWA',
					 'corn!',
					 '....................',
					 'also lol letting PCA run for 3.5 hours on corn overnight',
					 'Did you know RAGBRAI registration is open?',
					 'loooooooooooooooooooooooooooool',
					 'THERE ARE SO MANY COOL EE CLASSES AAAAAH',
					 'Tell me, have you seen... the marvelous Breadfish!!?',
					 'haar wavelets are silly',
					 'You know what this omlette needs? Cayenne peppers.',
					 'I think I am going to go practice violin now.',
					 'brb biking 70 miles',
					 'lol bike computer thinks i went 108.6mph',
					 'herp',
					 'derp',
					 'merp',
					 'CHICKA CHICKA BOOM BOOM WILL THERE BE ENOUGH ROOM?',
					 'bill nye has ridden a bicycle from seattle to spokane in one day',
					 'hm i just found a paper i wrote for ap english about my life as a garbageman',
					 'YO SUP A DEBZ U HAVIN\' A GEWD DAYYYYO?',
					 '...and now i\'m comparing national cuisine stuff to startups',
					 'NIIIIIIIIIIIIIII HAOOOOOOOOOOOOOOOOOOOOOOO',
					 'Should I dress as a trumpet player again for Halloween?',
					 'Maybe I should go practice viola. or go biking.',
					 'why can\'t I motivate myself to do work',
					 'cayenne peppers are weak',
					 'oh, did I tell you that I set a new speed record... 47.2',
					 'U JELLY BRO?',
					 'have you friended Boris\'s hair on Facebook yet?',
					 '229 is silly.',
					 'herp derp why am i not working on this problem set',
					 'heh',
					 'lol',
					 'lololol',
					 'bloop',
					 'convex optimization is pretty cool',
					 'Stephen Boyd is awesome.',
					 'wait where is Brad Osgood?',
					 'how silly',
					 'k',
					 'hmmm what is productivity?',
					 'what is prodictivity...? Baby don\'t hurt me, don\'t hurt me no more...',
					 'haha ha ha jack my swayg',
					 'thunder and lightning, very very frightening',
					 'butter butter butter butter',
					 'Would you like to ingest pepper through your nostrils?',
					 '什么？',
					 'bayg'
					]
	return random.choice(response_list)


def greet():
	print('Matt the Chat version 1.1, 12/1/13')
	print('A chatbot meant to emulate Matt Staib.')

def main():
	greet()
	try:
		while True:
			response = input('=> ')
			rxn = reaction(response)
			print(rxn)
			subprocess.Popen(['say', rxn])
	except KeyboardInterrupt:
		print('')

if __name__ == '__main__':
	main()
