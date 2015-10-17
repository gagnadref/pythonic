import time
import math
import sys

sqrts = [1/math.sqrt(x) for x in range(1,100)]

def import_image(filename):
	f = open(filename,"r")
	size = f.readline().split()
	m = int(size[0])
	n = int(size[1])
	image = [[] for row in range(m)]
	row = 0
	for line in f:
		image[row] = [0 if char=='*' else 1 for char in line[0:-1]]
		row += 1
	return m, n, image

def gain(i, j, r, original, current):
	gain = 0
	lose = 0
	for x in range(i,i+r):
		for y in range(j,j+r):
			if current[x][y]==0:
				if original[x][y]==1:
					gain+=1
				else:
					lose+=1
	return gain, lose

def gain1(i, j, r, original, current):
	g, l = gain(i, j, r, original, current)
	if g <= 1:
		return -float('inf')
	return g*sqrts[r-1]-l

def gain2(i, j, r, original, current):
	g, l = gain(i, j, r, original, current)
	if g - l <= 1:
		return -float('inf')
	return g*sqrts[r-1]-l

def paint(i, j, r, current):
	for x in range(i,i+r):
		for y in range(j,j+r):
			current[x][y]=1

def insert(squares,square,mini,maxi):
	g=(-square[3],square[2])
	mean = int(mini+(maxi-mini)/2)
	g2=(0,0)
	g2=(-squares[mean][3],squares[mean][2])
	g3=(-squares[mean-1][3],squares[mean-1][2])
	if (g>=g3 and g<=g2):
		squares.insert(mean,square)
	elif mini==maxi-1:
		squares.append(square)
	elif g>g2:
		insert(squares,square,mean,maxi)
	else:
		insert(squares,square,mini,mean-1)


def fast_painting(m, n, r_max, original):	
	current = [[0 for i in range(n)] for j in range(m)]
	squares = []
	painting = []
	t0 = time.time()
	for r in range(r_max,1,-1):
		for i in range(m-r+1):
			for j in range(n-r+1):
				g = gain2(i, j, r, original, current)
				if g > -float('inf'):
					squares.append((i,j,r,g))
	t1 = time.time()
	print(round(t1-t0,2))
	squares.sort(key=lambda x: (-x[3],x[2]))
	t2 = time.time()
	print(round(t2-t1,2))
	nb_squares = len(squares)
	print(nb_squares)
	s = 0
	while s < nb_squares:
		i,j,r,g=(squares[s][0],squares[s][1],squares[s][2],squares[s][3])
		g2 = gain2(i, j, r, original, current)
		if g == -float('inf'):
			pass
		elif g2 == g or g2>=squares[s+1][3]:
			paint(i, j, r, current)
			painting.append((i,j,r))
		else:
			insert(squares,(i,j,r,g2), s, nb_squares)
			nb_squares += 1
		s+=1
	t3 = time.time()
	print(round(t3-t2,2))
	return painting, current

def finish_painting(m, n, painting, current, original):
	t4 = time.time()
	for i in range(m):
		for j in range(n):
			if current[i][j] != original[i][j]:
				if current[i][j] == 0:
					painting.append((i,j,1))
					current[i][j] = 1
				else:
					painting.append((i,j,-1))
					current[i][j] = 0
	t5 = time.time()
	print(round(t5-t4,2))
	return painting

def export_result(painting, filename):
	with open(filename, 'w') as f:
		for paint in painting:
			if paint[2] == -1:
				f.write("ERASE,"+str(paint[1])+","+str(paint[0])+"\n")
			else:
				f.write("FILL,"+str(paint[1])+","+str(paint[0])+","+str(paint[2])+"\n")

if __name__ == "__main__":
	m, n, original = import_image("xyz.txt")
	ss_min = int(sys.argv[1]) if len(sys.argv) >= 2 else 10
	ss_max = int(sys.argv[2]) if len(sys.argv) >= 3 else ss_min+1
	for r in range(ss_min,ss_max):
		r_max = min(m,n,r)
		print(r_max)
		print(m)
		print(n)
		painting, current = fast_painting(m, n, r_max, original)
		painting = finish_painting(m, n, painting, current, original)
		print(len(painting))
		export_result(painting,"output.txt")