import unittest, pdb

class Board:
	import random
	def __init__(self, users = None, board_state= None):

		if users:
			random_pick = random.randint(0,1) 
			self.x = users[random_pick]
			self.o = users[random_pick - 1]
		else:
			self.x, self.o = self.get_usernames()

		if not board_state:
			self.blank_board()
		else: 
			self.board_state = board_state

		self.print_welcome()
		self.game_state = 'continue'
		self.gameplay()

	def __repr__(self):
		e = self.board_state
		output = f'''
		    a   b   c
		   --- --- ---
		1 | {e[0][0]} | {e[0][1]} | {e[0][2]} |
		   --- --- ---
		2 | {e[1][0]} | {e[1][1]} | {e[1][2]} |
		   --- --- ---
		3 | {e[2][0]} | {e[2][1]} | {e[2][2]} |
		   --- --- ---
		'''
	def blank_board(self):
		self.board_state = [[' ', ' ', ' '] for i in range(3)]

	def gameplay():
		self.evalulate_game()
		#maybe use switch for control flow here
		if self.game_state == 'win':
			print(f'{self.winner} has won!')
		elif self.game_state == 'draw':
			print(f'It\'s a draw. Play again?')	
		elif self.game_state == 'continue':
			
				
		
		#self.get_move()

	def evaluate_game(self):
		#note that self.evaluate_game also needs to add a winner attribute
		

	def get_usernames(self):
		#Note that self.get_usernames should randomly choose who's x and who's o
	
	def get_move(self):
	
if __name__ == '__main__':
	unittest.main()
	
class TestTicTac(unittest):
	def setup(self):
		self.board0 = Board(users = ['Nathan', 'Big Guy'],
						   board_state = [['o', 'o', 'x'],
						   				  ['x', 'o', 'x'],
										  ['x', ' ', 'o']])
		self.board0.evaluate_game()

		self.board1 = Board(users = ['Nathan', 'Big Guy'],
						   board_state = [['x', 'o', 'x'],
						   				  ['x', 'o', 'o'],
										  ['x', ' ', ' ']])
		self.board1.evaluate_game()

		self.board2 = Board(users = ['Nathan', 'Big Guy'],
						   board_state = [['x', 'o', 'x'],
						   				  ['x', 'o', 'o'],
										  ['o', 'x', 'x']])
		self.board2.evaluate_game()

		self.board3 = Board(users = ['Nathan', 'Big Guy'],
						   board_state = [['x', 'o', 'x'],
						   				  ['o', 'x', 'o'],
										  ['x', ' ', ' ']])
		self.board3.evaluate_game()

	def test_evaluate_game(self):
		self.assertEqual(self.board0.evaluate_game(), 'win', 'There should be a winner for board0')
		self.assertEqual(self.board0.winner, self.o, 'Board 0 winner should be o')

		self.assertEqual(self.board1.evaluate_game(), 'win', 'There should be a winner for board1')
		self.assertEqual(self.board1.winner, self.x, 'Board 1 winner should be x')
		
		self.assertEqual(self.board2.evaluate_game(), 'draw', 'There should be a draw for board2')
		self.assertEqual(self.board2.winner, None, 'None should be value of board2.winner')

		self.assertEqual(self.board3.evaluate_game(), 'continue', 'This game should continue')
		self.assertEqual(self.board3.winner, None, 'None should be value of board3.winner')

	def test_gameplay(self):
		#should determine whose turn it is based on number of x's and o's, assuming
		#that x always moves first, and prompt the appropriate player to move

		#
