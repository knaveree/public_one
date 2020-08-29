import unittest, pdb
import random, re

class Board(object):
	
	help_string = '''
		The interface responds to the following commands:

			In Gameplay Mode:

		b1, 2c, 3a: or any two digit combination of a,b,c and 1,2,3 to 
					select a square for your mark.

		quit or q:	Abandon the game and leave the interface because you've 
					remembered you could be doing literally anything else 
					and it would be a better use of your time.

		save or s:  Save the game (but y tho?) to a file.  Feature under 
					development. Does nothing currently.

		new or n:	Enters startup mode and prompts you to either keep 
					players and marks as is, or keep players with the same 
					marks, switch marks, or randomly select new marks. If 
					a game is underway, you have the option of keeping the 
					board or starting a new one.  

		help or h:	prints this. but you're here, so you already know that. 
	
		blurb or b: If you're even worse at finding ways to occupy yourself
					than your presence here would suggest, which is would be
					really remarkable, you could read this.

			In Startup Mode:

		quit or q: 	Same as in Gameplay mode. And still the best choice.
	
		new or n: 	Restarts startup mode and wipes away all entries made
					in prior startup mode. Preexisting game state remains 
					unchanged.

		help or h:  Do I need to say this again?	

		blurb or b: Try it. I dare you.
		'''
		
	blurb_string = '''
		So you've decided to play Tic-Tac_Toe, a game that has bored
		generations of Americans (and Canadians, and whatever other
		countries are allegedly out there) and is almost certain to 
		bore you too! 

		Seriously, how did you even find this app?
		
		So here's the deal. When you enter your names, you are 
		randomly assigned to x or o. Sorry, that's mandatory. I am a 
		capricious God of my Python universe and you'll just have 
		to deal with my edicts.

		Type a1 for square a1. Or b2 for square b2. 
		If you want, you can throw in a bunch of extra stuff, because
		the app uses Regex to pluck out any two digit combination of a letter
		and a number between 1-3 and a-c respectively. 

		This makes it a little harder to mess up your incredibly 
		exciting Tic-Tac-Toe game with a typo. I mean gawd, what
		a tragedy that would be.

		Have fun.
	'''

	def __init__(self, users = None, board_state= None):
		if users:
			random_pick = random.randint(0,1) 
			self.x = users[random_pick]
			self.o = users[(random_pick - 1) % 2]
		else:
			self.x, self.o = self.get_usernames()

		if not board_state:
			self.blank_board()
		else: 
			self.board_state = board_state

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
		return output

	def blank_board(self):
		self.board_state = [[' ', ' ', ' '] for i in range(3)]

	def count_moves(self):
		x_count, o_count = 0,0
		for row in self.board_state:
			x_count += row.count('x')
			o_count += row.count('o')
		return {'x': x_count,
				'o': o_count,
				'total': x_count + o_count}

	def determine_turn(self):
		return self.x if self.count_moves()['x'] == self.count_moves()['o'] else self.o 	
		
	def gameplay(self):
		self.evalulate_game()
		#maybe use switch for control flow here

		if self.game_state == 'win':
			print(f'{self.winner} has won!')

		elif self.game_state == 'draw':
			print(f'It\'s a draw!')	

		elif self.game_state == 'continue':
			print(f'{self.determine_turn()}, it\'s your turn!')			

			user_input = input()
			if user_input == 'h' or 'help':
				print(Board.help_string)
				#this method still under development
		
		#self.get_move()

	def sum_along_path(self, line_type, axis, mark):
		if line_type == 'row':
			return self.board_state[axis].count(mark)
		elif line_type == 'column':
			return [column[axis] for column in self.board_state].count(mark)
		elif line_type == 'diagonal':
			diagonal = lambda i, axis: self.board_state[2*(axis%2) +((-1)**axis)*i][i] 
			return [diagonal(i, axis) for i in range(3)].count(mark)

	def evaluate_game(self):
		self.game_state = 'continue'
		self.winner = None
		for line_type in ['diagonal','column', 'row']:
			if self.game_state == 'win':
				break
			for mark in ['x','o']:
				evaluations = [self.sum_along_path(line_type, axis, mark) for axis in range(3)]
				if 3 in evaluations: 
					self.winner = self.__dict__[mark]
					print(self.winner)
					self.game_state = 'win'
					print(self.game_state)
					break
		if not self.winner and self.count_moves()['total'] == 9:
			self.game_state = 'draw'
			
	def print_welcome(self):
		print(f'Welcome {self.x} and {self.o}!')
		print(f'{self.x} is X and goes first.')
		
#	def get_usernames(self):
#		#Note that self.get_usernames should randomly choose who's x and who's o
#	
#	def get_move(self):
	
	
class TestTicTac(unittest.TestCase):
	def setUp(self):
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
	
	def test_count_moves(self):
		self.assertEqual(self.board0.count_moves()['x'],4)
		self.assertEqual(self.board0.count_moves()['o'], 4)
		self.assertEqual(self.board0.count_moves()['total'],8)

	def test_determine_turn(self):
		self.assertEqual(self.board3.determine_turn(), self.board3.o)
		self.assertEqual(self.board2.determine_turn(), self.board2.o)
		self.assertEqual(self.board1.determine_turn(), self.board1.o)
		self.assertEqual(self.board0.determine_turn(), self.board0.x)

	def test_sum_along_diagonal(self):
		self.assertEqual(self.board0.sum_along_path('diagonal', 0, 'o'), 3, 'board0 main diagonal should sum to 3')
		self.assertEqual(self.board0.sum_along_path('diagonal', 1, 'o'), 1, 'board0 anti-diagonal should sum to 1')
		self.assertEqual(self.board0.sum_along_path('diagonal', 2, 'o'), 3, 'second reference to main should match')
		self.assertEqual(self.board0.sum_along_path('diagonal', 0, 'x'), 0, 'x diagonal should complement')
		self.assertEqual(self.board0.sum_along_path('diagonal', 1, 'x'), 2, 'x  anti-diagonal should complement')
		self.assertEqual(self.board0.sum_along_path('diagonal', 2, 'x'), 0, 'second reference to main should match')

	def test_sum_along_row(self):
		self.assertEqual(self.board3.sum_along_path('row', 0, 'o'), 1, 'board3 main row should sum to 1')
		self.assertEqual(self.board3.sum_along_path('row', 1, 'o'), 2, 'board3 mid row should sum to 1')
		self.assertEqual(self.board3.sum_along_path('row', 2, 'o'), 0, 'board3 last row should sum to 0')  
		self.assertEqual(self.board3.sum_along_path('row', 0, 'x'), 2, 'x row should complement')
		self.assertEqual(self.board3.sum_along_path('row', 1, 'x'), 1, 'x  anti-row should complement')
		self.assertEqual(self.board3.sum_along_path('row', 2, 'x'), 1, 'second reference to main should match')

	def test_sum_along_column(self):
		self.assertEqual(self.board3.sum_along_path('column', 0, 'o'), 1, 'board3 main column should sum to 3')
		self.assertEqual(self.board3.sum_along_path('column', 1, 'o'), 1, 'board3 anti-row should sum to 1')
		self.assertEqual(self.board3.sum_along_path('column', 2, 'o'), 1, 'second reference to main should match')
		self.assertEqual(self.board3.sum_along_path('column', 0, 'x'), 2, 'x column should complement')
		self.assertEqual(self.board3.sum_along_path('column', 1, 'x'), 1, 'x column should complement')
		self.assertEqual(self.board3.sum_along_path('column', 2, 'x'), 1, 'second reference to main should match')

	def test_evaluate_game(self):
		self.assertEqual(self.board0.game_state, 'win', 'There should be a winner for board0')
		self.assertEqual(self.board0.winner, self.board0.o, 'Board 0 winner should be o')

		self.assertEqual(self.board1.game_state, 'win', 'There should be a winner for board1')
		self.assertEqual(self.board1.winner, self.board1.x, 'Board 1 winner should be x')
		
		self.assertEqual(self.board2.game_state, 'draw', 'There should be a draw for board2')
		self.assertEqual(self.board2.winner, None, 'None should be value of board2.winner')

		self.assertEqual(self.board3.game_state, 'win', 'This game should have a winner')
		self.assertEqual(self.board3.winner, self.board3.x, 'Winner listed here')
#
	
#	def test_gameplay(self):
		#should determine whose turn it is based on number of x's and o's, assuming
		#that x always moves first, and prompt the appropriate player to move
		#

if __name__ == '__main__':
	unittest.main()