import pygame as pg
import random

class Sand:
	''' 
	Object to store data from each indivisual grain of sand
	'''
	def __init__(self, color: set):
		self.color = color
		return

def isValidIndex(x: int, y: int):
	'''
	Check positional index values of a grain of sand
	'''
	return (x>=0) and (x<nX) and (y>=0) and (y<nY)

def adjustColor():
	'''
	Adjust global RGB values while mouse being pressed 
	'''
	for channel in COLORS:
		COLORS[channel] += random.choice([-1, 1])*random.randint(1, 5)

		if COLORS[channel]>255 or COLORS[channel]<0:
			COLORS[channel] = random.randint(0, 255)
	return

def applyColor(grid: list):
	pos = pg.mouse.get_pos()

	x = int(nX*pos[0]/WIDTH)
	y = int(nY*pos[1]/HEIGHT)

	if isValidIndex(x, y):
		color = (
			COLORS["R"],
			COLORS["G"],
			COLORS["B"],
		)

		grid[y][x] = Sand(color)
	return

def update(grid: list):
	''' Iterate through each cell in the grid '''
	for i in range(nY-1, -1, -1):
		for j in range(nX):
			cell = grid[i][j]

			''' If not sand object'''
			if not isinstance(cell, Sand):
				continue

			''' If invalid position '''
			if not isValidIndex(j, i+1):
				continue

			''' If the cell below is empty, move sand object down '''
			if grid[i+1][j]==0:
				grid[i+1][j] = cell 
				grid[i][j] = 0
			else:
				dirs = [-1, 1] 
				random.shuffle(dirs)

				''' If either of the diagonally below cells is empty, move sand object down '''
				for _dir in dirs:
					if not isValidIndex(j+_dir, i+1):
						continue

					if grid[i+1][j+_dir]==0:
						grid[i+1][j+_dir] = cell
						grid[i][j] = 0
	return

def render(grid: list):
	for i in range(nY):
		for j in range(nX):
			if isinstance(grid[i][j], Sand):
				pg.draw.rect(window, grid[i][j].color, (j*xSize, i*ySize, xSize, ySize), 3)	
				#pg.draw.circle(window, grid[i][j].color, (j*xSize, i*ySize), 5)
	return

def main():
	''' Grid used to store all sand objects '''
	grid = [[0 for _ in range(nX)] for _ in range(nY)]

	is_running = True
	while is_running:
		for event in pg.event.get():
			if event.type==pg.QUIT:
				is_running = False
				break

		window.fill(BLACK)

		''' Generate grains of sand using mouse '''
		click = pg.mouse.get_pressed()
		if any(click):
			adjustColor()
			applyColor()

		''' Update positions of each grain of sand '''
		update(grid)

		''' Render sand '''
		render(grid)

		pg.display.flip()

	pg.quit()
	return

if __name__=="__main__":
	WIDTH = 800
	HEIGHT = 400 

	''' Maximum number of sand objects for each direction within grid '''
	nX = 100 
	nY = 100 

	''' width and height of sand object '''
	xSize = float(WIDTH/nX)
	ySize = float(HEIGHT/nY)

	''' Global RGB variables to apply color '''
	COLORS = {
		"R": 150,
		"G": 100,
		"B": 80,
	}

	pg.init()
	window = pg.display.set_mode((WIDTH, HEIGHT))
	pg.display.set_caption("Sand Simulation")

	main()

