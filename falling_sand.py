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

def toggleObstacle(grid: list, value: int):
	pos = pg.mouse.get_pos()

	x = int(nX*pos[0]/WIDTH)
	y = int(nY*pos[1]/HEIGHT)

	if isValidIndex(x, y):
		if not isinstance(grid[y][x], Sand):
			grid[y][x] = value
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

			if grid[i+1][j]==0:
				''' If the cell below is empty, move sand object down '''
				grid[i+1][j] = cell 
				grid[i][j] = 0
			else:
				''' 
				By DENSITY probability, stack current Sand object on top of the bottom one.
				The Sand objects behave like smooth fluid or solid particles depending on this value.
				'''
				if random.random()<DENSITY:
					continue

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
			elif grid[i][j]==1:
				pg.draw.rect(window, WHITE, (j*xSize, i*ySize, xSize, ySize), 3)	
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

		click = pg.mouse.get_pressed()
		if click[0]:
			''' 
			Generate grains of sand using left mouse button.
			Colors change per frame while button being pressed.
			'''
			adjustColor()
			applyColor(grid)
		elif click[1]:
			''' Delete obstacles using middle mouse button '''
			toggleObstacle(grid, 0)	
		elif click[2]:
			''' Generate obstacles using right mouse button '''
			toggleObstacle(grid, 1)	

		''' Update positions of each grain of sand '''
		update(grid)

		''' Render sand '''
		render(grid)

		pg.display.flip()

	pg.quit()
	return

if __name__=="__main__":
	WIDTH = 800
	HEIGHT = 800 

	''' Tendency of sand objects trying to stack on top of another '''
	DENSITY = 0.9

	''' Maximum number of sand objects for each direction within grid '''
	nX = 200 
	nY = 200 

	''' width and height of sand object '''
	xSize = float(WIDTH/nX)
	ySize = float(HEIGHT/nY)

	''' Global RGB variables to apply color '''
	COLORS = {
		"R": 150,
		"G": 100,
		"B": 80,
	}

	WHITE = (255, 255, 255)
	BLACK = (0, 0, 0)

	pg.init()
	window = pg.display.set_mode((WIDTH, HEIGHT))
	pg.display.set_caption("Sand Simulation")

	main()

