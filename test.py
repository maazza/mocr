from random import choice, random

unit_step = lambda x: 0 if x < 0 else 1

def dot(a,b):
	return sum( [a[i]*b[i] for i in range(len(b))])
	
w=[1 - random()*2 for x in range(3)]

eta = 0.2
n = 100
t = [([0,0,1],0),([1,0,1],1),([0,1,1],1),([1,1,1],1)]
errors = []

for x, _ in t:
	    result = dot(x, w)
	    print("{}: {} -> {}".format(x[:2], result, unit_step(result)))


for i in range(n):
	    x, expected = choice(t)
	    result = dot(w, x)
	    error = expected - unit_step(result)
	    errors.append(error)
	    w[0] += eta * error * x[0]
	    w[1] += eta * error * x[1]
	    w[2] += eta * error * x[2]

for x, _ in t:
	    result = dot(x, w)
	    print("{}: {} -> {}".format(x[:2], result, unit_step(result)))
