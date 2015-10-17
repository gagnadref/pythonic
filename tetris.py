import PIL.Image as Image
import numpy as np

def parse(filename):
	f = open(filename)
	piece = [""]
	data = [1,2]
	pieces = []
	for line in f:
		if not(line[0] in ["#", "*"]):
			pieces.append({'id': int(data[0]), 'q': int(data[1]), 'h': len(piece), 'w': len(piece[0]), 's': piece})
			data = line.strip('\n').split(',')
			piece = []
		else:
			piece.append(list(line.strip('\n')))
	pieces.append({'id': int(data[0]), 'q': int(data[1]), 'h': len(piece), 'w': len(piece[0]), 's': piece})
	return pieces[1:]

def toBits(pieces):
	for p in pieces:
		piece = p['s']
		piece = [[0 if piece[i][j] == "*" else 1 for j in range(0,p['w'])] for i in range(0,p['h'])]
		p['s'] = piece
	return pieces

def sum2d(list):
    return sum(map(sum, list))

def getComplexity(piece):
	return (piece['h']*piece['w'],piece['h']*piece['w']-sum2d(piece['s']))

def sortByComplexity(pieces):
	return sorted(pieces, key=lambda p: getComplexity(p), reverse=True)

def explode(pieces):
	exploded = []
	for p in pieces:
		for n in range(p['q']):
			exploded.append(p)
	return exploded

def fill(pieces, square, h, w):
	actions = []
	i = 0
	for p in pieces:
		if i%100 == 0:
			print(i)
			saveAsImage(square)
		square, actions = place(p, square, actions, h, w)
		i+=1
	return actions, square

def place(piece, square, actions, h, w):
	for i in range(0,h):
		for j in range(0,w):
			if isAllowed(square, piece, i, j, h, w):
				actions.append((piece['id'],j,i))
				square = addPiece(piece, square, i, j)
				return square, actions
	return square, actions

def isAllowed(square, piece, i, j, h, w):
	if i+piece['h'] > h or j+piece['w'] > w:
		return False
	for y in range(0, piece['h']):
		for x in range(0, piece['w']):
			if piece['s'][y][x] and square[i+y][j+x]:
				return False
	return True

def addPiece(piece, square, i, j):
	for y in range(0, piece['h']):
		for x in range(0, piece['w']):
			square[i+y][j+x] = (square[i+y][j+x] or piece['s'][y][x])
	return square

def export(actions, filename):
	with open(filename, 'w') as f:
		for action in actions:
			f.write(",".join(map(str,action)) + "\n")

def saveAsImage(square):
	img = Image.fromarray(255*np.asarray(square, dtype=np.uint8))
	img.save('my.png')

if __name__ == "__main__":
	pieces = parse("tetris.txt")
	pieces = toBits(pieces)
	pieces = explode(pieces)
	print(len(pieces))
	pieces = sortByComplexity(pieces)
	h = 200
	w = 200
	actions, square = fill(pieces, [[0 for j in range(0, w)] for i in range(0,h)], h, w)
	export(actions, "tetrisout.txt")
