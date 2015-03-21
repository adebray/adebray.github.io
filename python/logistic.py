#Going to graph a logistic curve.

from Tkinter import *

def main():
    master = Tk()
    w = Canvas(master,width=500,height=500)
    w.pack()
    #w.create_line(0,0,200,200)
    #create_point(50,100,w)
    #the x-scale is 0 to 10, so each pixel is 0.02. Maybe constants here?
    #the y-scale is 0 to 1, so each pixel is 0.002.
    x = 1.0
    while x < 5:
    #for x in range(0.0,10.0,2e-2):
	to_graph = logistic_array(x)
	for y in to_graph:
	    create_point(pixel_of_x(x),pixel_of_y(y),w)
	x = x + 0.005 #will be 0.02
	

def create_point(a,b,w): #Is there really no create_point function?
    w.create_line(a,b,a+1,b)
    w.create_line(a+1,b,a+2,b,fill="white")

def logistic_array(x):
    to_ret = []
    a = 0.2 #Starting value for the 
    for i in range(0,5000):
	a = x*a*(1-a)
	if i > 4000: #Unintentional, I promise
	    to_ret.append(a)
    return to_ret

def pixel_of_x(x):
    return 170*(x-1)

def pixel_of_y(y):
    return 500*(1-y)
    
if __name__ == '__main__':
    main()
