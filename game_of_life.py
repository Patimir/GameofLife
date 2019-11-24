import pygame
import random
import sys

class LifeGame:
	BLACK = 0, 0, 0
	CYAN = 0, 255, 255
	RED = 255, 0, 0

	def __init__(self, screen_width=800, screen_height=600, cell_size=10, shape='circle'):
		'''
		Initialize the grid, set default game state, initialize screen

		:param screen_width: Game window width
		:param screen_height: Game window height
		:param cell_size: Size of the individual cells
		:param shape: Shape of the individual cells
		'''
		self.screen_height = screen_height
		self.screen_width = screen_width
		self.cell_size = cell_size
		self.shape = shape
		self.pause = False

		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
		self.clear_screen()

		self.num_cols = self.screen_width // self.cell_size
		self.num_rows = self.screen_height // self.cell_size

		self.init_grids()
		self.set_grid()


	def init_grids(self):
		'''
		Initialize active and inactive grid
		Initial grid is a simple python 2D list filled with 0's 

		:return: None
		'''
		self.active_grid = [x[:] for x in [[0] * self.num_cols] * self.num_rows]
		self.inactive_grid = [x[:] for x in [[0] * self.num_cols] * self.num_rows]


	def set_grid(self, value=None):
		'''
		Set grid values to (0 or 1) If value == None randomize the grid

		Example:
			set_grid(0) -> all dead
			set_grid(1) -> all alive
			set_grid(), set_grid(None) -> random

		:param value: set the cell value to (0 or 1)
		:return: None
		'''
		for row in range(self.num_rows):
			for col in range(self.num_cols):
				if value is None:
					cell_value = random.choice([0, 1])
				else:
					cell_value = value
				self.active_grid[row][col] = cell_value


	def draw_grid(self):
		'''
		Given the grid, cells state and shape, draw the cells on the screen

		:return: None
		'''
		self.clear_screen()
		for row in range(self.num_rows):
			for col in range(self.num_cols):
				if self.active_grid[row][col] == 1:
					colour = self.RED
				else:
					colour = self.BLACK

				if self.shape == None or self.shape == 'square':
					pygame.draw.rect(self.screen, colour, 
								    (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))
				elif self.shape == 'circle':
					pygame.draw.circle(self.screen, colour, 
								      (col * self.cell_size + self.cell_size//2, row * self.cell_size + self.cell_size//2), 
								      self.cell_size//2)
		pygame.display.flip()


	def clear_screen(self):
		'''
		Fill the whole screen with black color (clear the screen)

		:return: None
		'''
		self.screen.fill(self.BLACK)


	def count_live_neighbors(self, row, col):
		'''
		Count the number of live adjacent cells given row and column index

		:param row: row index
		:param col: column index
		:return: int: number of live cells 
		'''
		count = 0
		if (row > 0 and self.active_grid[row - 1][col] == 1): 
			count += 1
		if (col > 0 and self.active_grid[row][col - 1] == 1): 
			count += 1
		if (row > 0 and col > 0 and 
			self.active_grid[row - 1][col - 1] == 1): 
			count += 1
		if (row < self.num_rows - 1 and self.active_grid[row + 1][col] == 1): 
			count += 1
		if (col < self.num_cols - 1 and self.active_grid[row][col + 1] == 1): 
			count += 1
		if (row < self.num_rows - 1 and col < self.num_cols - 1
			and self.active_grid[row + 1][col + 1] == 1): 
			count += 1
		if (row < self.num_rows - 1 and col > 0
			and self.active_grid[row + 1][col - 1] == 1): 
			count += 1
		if (row > 0 and col < self.num_cols - 1
			and self.active_grid[row - 1][col + 1] == 1): 
			count += 1

		return count


	def check_cell_neighbours(self, row, col):
		'''
		Determines whether next generation cell will live or die based on the rules:
		# 4 rules: Underpopulation, Overpopulation, Reproduction, Survival

		:param row: row index
		:param col: column index
		:return: True or False
		'''
		num_alive_neighbors = self.count_live_neighbors(row, col)
		if self.active_grid[row][col] == 1: # Alive cell
			if num_alive_neighbors < 2: # Underpopulation
				return False
			if num_alive_neighbors > 3: # Overpopulation
				return False
			if num_alive_neighbors == 2 or num_alive_neighbors == 3: # Survives
				return True
		if self.active_grid[row][col] == 0: # Dead cell
			if num_alive_neighbors == 3: # Reproduction
				return True
			else:
				return False


	def update_generation(self):
		'''
		Inspect the current generation, update inactive grid and swap out the grids
		
		:return: updated active_grid
		'''
		for row in range(self.num_rows):
			for col in range(self.num_cols):
				if self.check_cell_neighbours(row, col):
					self.inactive_grid[row][col] = 1
				else:
					self.inactive_grid[row][col] = 0

		self.active_grid = self.inactive_grid
		return self.active_grid


	def handle_events(self):
		'''
		Handle eny key presses
		s / space -> start/stop
		r 		  -> randomize grid
		q / esc   -> quit the game
		1 		  -> fill the screen with live cells only
		0 		  -> fill the screen with dead cells only

		:return: None
		'''
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q or event.type == pygame.K_ESCAPE:
					sys.exit()
				if event.key == pygame.K_r:
					self.set_grid(None)
				if event.key == pygame.K_1:
					self.set_grid(1)
				if event.key == pygame.K_0:
					self.set_grid(0)
				if event.key == pygame.K_s or event.key == pygame.K_SPACE:
					if self.pause:
						self.pause = False
					else:
						self.pause = True


	def run(self):
		'''
		Run the main game until forever until quit state

		:return: None
		'''
		clock = pygame.time.Clock()
		while True:
			clock.tick(10)

			self.handle_events()
			if self.pause:
				self.draw_grid()
				continue

			self.update_generation()
			self.draw_grid()