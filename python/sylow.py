#!/usr/bin/python

#Arun Debray, 11 December 2012

#does a quick, stupid check to see if a group of a given order can be simple.
#Usage: ./sylow.py order, or ./sylow.py -v order for more information.

import sys
import math

def main():
    flags = 0
    if len(sys.argv) < 2:
	print "Usage: ./sylow.py order"
	print "Flags: -v verbose"
	sys.exit(1)
    if sys.argv[1] == '-v':
	print "Verbose mode enabled."
	if len(sys.argv) < 3:
	    print "Usage: ./sylow.py -v order"
	    sys.exit(1)
	flags = 1
    order = int(sys.argv[1 + flags])
    check(order,flags)

def check(order,flags):
    factorList = factors(order)
    if (flags == 1):
	sys.stdout.write("Factors: ")
	for prime in factorList:
	    sys.stdout.write(str(prime) + " ")
	sys.stdout.write("\n")
    checkForFactorial(order)
    if len(factorList) == 1:
	print "A simple group of order " + str(order) + " exists, and is \033[1;30mZ\033[0m/" + str(order) + "\033[1;30mZ\033[0m."
    else:
	currentCount = 0
	for prime in factorList:
	    alpha = factorList.count(prime)
	    m = order / alpha
	    if alpha == 1: #all I can do for now
		currentCount += numOfOrder(order,m,prime,flags)
	if flags == 1:
	    print "Found " + str(currentCount) + " elements if simple, which means that:"
	if currentCount > order:
	    print "There is no simple group of order " + str(order) + "."
	else:
	    print "This test was inconclusive."

def checkForFactorial(order):
    factSoFar = 1
    i = 1
    while factSoFar < order:
	i += 1
	factSoFar *= i
	if 2*order == factSoFar and i > 4:
	    if i > 9:
		print "A simple group of order " + str(order) + " exists, and is A_{" + str(i) + "}."
	    else:
		print "A simple group of order " + str(order) + " exists, and is A_" + str(i) + "."
	    sys.exit(0)

#assumes alpha = 1
def numOfOrder(order,m,prime,flags):
    divisorList = divisors(m)
    #print divisorList
    #print [x%prime for x in divisorList]
    options = filter(lambda x: x%prime == 1,divisorList)
    if len(options) == 0:
	if (flags == 1):
	    print "There is necessarily a normal subgroup of order " + str(prime) + "."
	print "There is no simple group of order " + str(order) + "."
	sys.exit(0)
    bestCase = min(options)
    if flags == 1:
	print "There are at least " + str(bestCase * (prime - 1)) + " elements of order " + str(prime) + "."
    return bestCase * (prime - 1) #there's that many of that order
    

def factors(n):
    toReturn = []
    #for i in range(math.ceil(math.sqrt(n))):
    i = 2
    while True:
	if n == 1: break
	if n%i == 0:
	    toReturn.append(i)
	    n = n/i
	    i = 2
	else:
	    i += 1
    return toReturn

def divisors(n):
    toReturn = []
    #for i in range(2,1+int(math.ceil(math.sqrt(n)))):
    for i in range(2,n+1):
	if n%i == 0:
	    toReturn.append(i)
    #toReturn.append(n)
    return toReturn

if __name__ == '__main__':
    main()
