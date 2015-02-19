"""
Author: Robert Bond <rjb8682@rit.edu>
File: puzzle.py
Description: This program will allow the user to play the 8-puzzle
			 game through the command line


|-------|
|1| 2| 3|
|-------|
|4| 5| 6|
|-------|
|7| 8|  |
|-------|

|----------|
|1| 2| 3| 4|
|----------|
|1| 2| 3| 4|
|----------|
|1| 2| 3| 4|
|----------|
|1| 2| 3| 4|
|----------|




"""
from random import shuffle
from copy import deepcopy
import os
import sys

board = None
dirs = ['w', 's', 'a', 'd']

def getEmpty(boardArray):

	for row in range(len(boardArray)):
		for col in range(len(boardArray)):
			if boardArray[row][col] == ' ':
				return (row, col)

	return None

def createWins():
	numbers = [i for i in range(1, board.size * board.size)]
	numbers.append(' ')
	win1 = [[numbers.pop(0) for col in range(board.size)] for row in range(board.size)]

	numbers = [' ']
	numbers.extend([i for i in range(1, board.size * board.size)])
	win2 = [[numbers.pop(0) for col in range(board.size)] for row in range(board.size)]

	numbers = [i for i in range(1, board.size * board.size)]
	numbers.append(' ')
	win3 = [[numbers.pop(0) for col in range(board.size)] for row in range(board.size)]
	for i in range(board.size):
		win3[i].reverse()

	numbers = [' ']
	numbers.extend([i for i in range(1, board.size * board.size)])
	win4 = [[numbers.pop(0) for col in range(board.size)] for row in range(board.size)]
	for i in range(board.size):
		win4[i].reverse()

	wins = [win1, win2, win3, win4]

	return wins

class gameBoard:
	"""
	Represents the gameboard. Holds the whole board plus the current
	empty spot.
	"""

	__slots__ = ('board', 'size', 'emptyPos', 'win')

	def __init__(self, size):
		"""
		Shuffles numbers and places them in the gameboard
		"""
		numbers = [i for i in range(1, size * size)]
		numbers.append(' ')
		shuffle(numbers)
		newBoard = [[numbers.pop(0) for col in range(size)] for row in range(size)]
		
		self.board = newBoard
		self.size = size
		self.emptyPos = getEmpty(newBoard)

	def __str__(self):
		"""
		Returns the string representation of the game board
		"""
		maxDigitLength = len(str(self.size**2))

		result = '|'

		result += '-' * ((self.size * (2 + maxDigitLength)) - 2) + '|\n'

		for row in board.board:
			result += '|' + "| ".join([str(i) + " " * (maxDigitLength - len(str(i))) for i in row]) + '|\n|'
			result += '-' * ((self.size * (2 + maxDigitLength)) - 2) + '|\n'

		return result

def drawScreen():
	os.system('cls' if os.name == 'nt' else 'clear' )
	print('Python - Number Puzzle')
	print('\n')
	print(board)

def checkWin():
	return board.board in board.win

def move(dir):
	"""
	"""

	emptyX = board.emptyPos[0]
	emptyY = board.emptyPos[1]

	if dir == 's':
		if (emptyX - 1) >= 0:
			temp = board.board[emptyX - 1][emptyY]
			board.board[emptyX][emptyY] = temp
			board.board[emptyX - 1][emptyY] = ' '
			board.emptyPos = (emptyX - 1, emptyY)
	elif dir == 'w':
		if (emptyX + 1) < board.size:
			temp = board.board[emptyX + 1][emptyY]
			board.board[emptyX][emptyY] = temp
			board.board[emptyX + 1][emptyY] = ' '
			board.emptyPos = (emptyX + 1, emptyY)
	elif dir == 'd':
		if (emptyY - 1) >= 0:
			temp = board.board[emptyX][emptyY - 1]
			board.board[emptyX][emptyY] = temp
			board.board[emptyX][emptyY - 1] = ' '
			board.emptyPos = (emptyX, emptyY - 1)
	elif dir == 'a':
		if (emptyY + 1) < board.size:
			temp = board.board[emptyX][emptyY + 1]
			board.board[emptyX][emptyY] = temp
			board.board[emptyX][emptyY + 1] = ' '
			board.emptyPos = (emptyX, emptyY + 1)
	else:
		print('Not a valid direction')
	
	drawScreen()

def printHelp():
	os.system('cls' if os.name == 'nt' else 'clear')
	drawScreen()
	print('To play:')
	print('\tEnter a command for it to run unless not on windows.')
	print('\t\tIf not on windows, type command then press enter.')
	print()
	print('Commands:')
	print("\t'w'/'a'/'s'/'d' - Moving the empty space")
	print("\t'esc (on windows) or 'b'' - exit the progam")
	print("\t'?' - for this list\n")

class _Getch:
	"""
	Gets a single character from standard input.  Does not echo to the
	screen.
	"""
	def __init__(self):
		self.impl = _GetchWindows()

	def __call__(self): return self.impl()

class _GetchWindows:
	def __init__(self):
		import msvcrt

	def __call__(self):
		import msvcrt
		return msvcrt.getch()

def main():
	os.system("title " + "Python - Number Puzzle")

	global board
	os.system('cls' if os.name == 'nt' else 'clear')
	if len(sys.argv) == 1:
		size = int(input('What size board? '))
	else:
		size = int(sys.argv[1])
	board = gameBoard(size)
	board.win = createWins()
	drawScreen()
	if os.name == 'nt':
		get = _Getch()
	else:
		get = None

	while True:
		cmd = None
		if get != None:
			cmd = str(get())[-2]
		else:
			cmd = input()

		process = processInput(cmd)

		if process == 0:
			return
		
		if checkWin():
			print('Awesome! You beat the puzzle!\nPlay again for a new random configuration')
			return

def processInput(command):
	if command in ['?',  'help']:
		printHelp()
	elif command in dirs:
		move(command)
	elif command == 'b':
		os.system('cls' if os.name == 'nt' else 'clear')
		return 0
	else:
		print("Not a command. Type '?' or 'help' for a list of commands")

if __name__ == '__main__':
	main()
