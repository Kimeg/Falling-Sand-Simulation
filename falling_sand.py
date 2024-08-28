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

def adjustColor(SAND_SIZE: int):
	'''
	Adjust global RGB values while mouse being pressed 
	'''
	for channel in COLORS:
		COLORS[channel] += random.choice([-1, 1])*random.randint(SAND_SIZE, 5*SAND_SIZE)

		if COLORS[channel]>255 or COLORS[channel]<0:
			COLORS[channel] = random.randint(0, 255)
	return

def toggleSand(grid: list, sand_size: int, nSand: int, mode: str):
	pos = pg.mouse.get_pos()

	x = int(nX*pos[0]/WIDTH)
	y = int(nY*pos[1]/HEIGHT)

	color = (
		COLORS["R"],
		COLORS["G"],
		COLORS["B"],
	)

	for i in range(sand_size*2+1):
		i -= sand_size

		for j in range(sand_size*2+1):
			j -= sand_size

			if isValidIndex(x+j, y+i):
				if mode=="ON":
					if grid[y+i][x+j]==0:
						grid[y+i][x+j] = Sand(color)
						nSand += 1
				elif mode=="OFF":
					if isinstance(grid[y+i][x+j], Sand):
						grid[y+i][x+j] = 0 
						nSand -= 1
	return nSand

def toggleObstacle(grid: list, obstacle_size: int, value: int, nObstacle: int):
	pos = pg.mouse.get_pos()

	x = int(nX*pos[0]/WIDTH)
	y = int(nY*pos[1]/HEIGHT)


	for i in range(obstacle_size*2+1):
		i -= obstacle_size

		for j in range(obstacle_size*2+1):
			j -= obstacle_size

			if isValidIndex(x+j, y+i):
				if not isinstance(grid[y+i][x+j], Sand):
					if value==1:
						if grid[y+i][x+j]==0:
							nObstacle += 1
					elif value==0:
						if grid[y+i][x+j]==1:
							nObstacle -= 1

					grid[y+i][x+j] = value
	return nObstacle

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

def renderText(value: str, x: int, y: int):
	ts = font.render(value, False, WHITE)
	window.blit(ts, (x, y))
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
	''' Resizes the area clicked for Sand object generation	'''
	SAND_SIZE = 1 

	''' Resizes the area clicked for obstacle generation '''
	OBSTACLE_SIZE = 1

	''' Total number of Sand objects '''
	nSand = 0

	''' Total number of Sand objects '''
	nObstacle = 0

	''' Generates Sand objects if mode=="on" else deletes them '''
	mode = "ON"

	''' Grid used to store all sand objects '''
	grid = [[0 for _ in range(nX)] for _ in range(nY)]

	is_running = True
	while is_running:
		for event in pg.event.get():
			if event.type==pg.QUIT:
				is_running = False
				break
			elif event.type==pg.KEYDOWN:
				if event.key==pg.K_a:
					if SAND_SIZE>1:
						SAND_SIZE -= 1 
				if event.key==pg.K_s:
					if SAND_SIZE<5:
						SAND_SIZE += 1
				if event.key==pg.K_z:
					if OBSTACLE_SIZE>1:
						OBSTACLE_SIZE -= 1
				if event.key==pg.K_x:
					if OBSTACLE_SIZE<5:
						OBSTACLE_SIZE += 1
				if event.key==pg.K_d:
					mode = "ON" if mode=="OFF" else "OFF"
				if event.key==pg.K_r:
					grid = [[0 for _ in range(nX)] for _ in range(nY)]
					nSand = 0
					nObstacle = 0

		window.fill(BLACK)

		click = pg.mouse.get_pressed()
		if click[0]:
			''' 
			Generate grains of sand using left mouse button.
			Colors change per frame while button being pressed.
			'''
			adjustColor(SAND_SIZE)
			nSand = toggleSand(grid, SAND_SIZE, nSand, mode)
		elif click[1]:
			''' Delete obstacles using middle mouse button '''
			nObstacle = toggleObstacle(grid, OBSTACLE_SIZE, 0, nObstacle)
		elif click[2]:
			''' Generate obstacles using right mouse button '''
			nObstacle = toggleObstacle(grid, OBSTACLE_SIZE, 1, nObstacle)

		''' Update positions of each grain of sand '''
		update(grid)

		''' Render sand '''
		render(grid)
		renderText(f"Total number of objects : {nSand+nObstacle}", 10, 10)
		renderText(f"Number of Sand objects  : {nSand}", 10, 30)
		renderText(f"Number of ostacles      : {nObstacle}", 10, 50)
		renderText(f"Sand cursor size        : {SAND_SIZE}", 10, 70)
		renderText(f"Obstacle cursor size    : {OBSTACLE_SIZE}", 10, 90)
		renderText(f"Sand toggle mode        : {mode}", 10, 110)

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
	pg.font.init()
	pg.display.set_caption("Sand Simulation")
	window = pg.display.set_mode((WIDTH, HEIGHT))
	font = pg.font.Font("lemon.ttf", 15)

	main()

