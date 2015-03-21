#Draws a Mandelbrot set.

from Tkinter import *

def main():
    master = Tk()
    w = Canvas(master,width=750,height=675)
    w.pack()
    a = -2.0
    while a < 1.75:
	b = -1.25 #Unfortunately this skips over zero
	while b < 1.25:
	    if in_set(a,b):
		create_point(give_x(a),give_y(b),w)
	    b = b + 0.001 #This takes a long time! You may want to use 0.004 instead
	a  = a + 0.001 #same thing

def in_set(a,b):
    z = (a,b)
    for i in range(100): #Hopefully sufficient
	z = next_fn(z,a,b)
    (x,y) = z
    if x*x + y*y < 3:
	return True
    else:
	return False

def next_fn(z,a,b):
    (x,y) = z
    x_next = x*x - y*y + a
    y_next = 2*x*y + b
    z_next = (x_next,y_next)
    return z_next

def create_point(a,b,w):
    w.create_line(a,b,a+1,b)
    w.create_line(a+1,b,a+2,b,fill="white")

def give_x(a):
    return 250*(a+2)

def give_y(b):
    return 250*(1.25-b)

if __name__ == '__main__':
    main()
