import unittest, pdb
import random, re
from unittest.mock import patch

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

		reboot or r:Enters startup mode and prompts you to either keep 
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
	
		reboot or r:Restarts startup mode and wipes away all entries made
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
	def blank_board(self):
		return [[' ', ' ', ' '] for i in range(3)]
	
	def __init__(self, users = None, board_state= None):
		'''
		TESTING FORMAT ONLY
		'''
		if users:
			self.x, self.o = (users[0], users[1])
		else:
			self.x, self.o = None, None
		
		if board_state:
			self.board_state = board_state
		else:
			self.board_state = self.blank_board()	

		self.quit, self.reboot = False, False
		self.evaluate_game()

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

	###UNTESTED###
	def save(self):
		'''
		UNFINISHED
		'''
		pass

	def random_assign(self, names_list):
		random_pick = random.randint(0,1)
		complement = (random_pick + 1) % 2
		self.x, self.o = names_list[random_pick], names_list[complement]
		return None

	def startup(self):
		prompt = '''
		Welcome to the single most boring game known to man. 
		'''
		print(prompt)
		names = list()
		for i in range(2):
			name = self.sanitize_input(f'Enter player {i+1} name', input_type = 'names')	
			names.append(name)
		random.shuffle(names)
		self.x, self.o = names[0], names[1]			
		self.board_state = self.blank_board()

	def update_board(self, square_id):
		'''
		Note that argument should be presanitized
		this should take an argument and use it to update the board
		'''
		mark = self.determine_turn(of = 'mark')
		y, x = (ord(square_id[0]) - 97, int(square_id[1]) - 1)

		if not self.board_state[x][y] == ' ':   
			print('This square is already occupied')	
			pass	
		else:	
			self.board_state[x][y] = mark
			self.evaluate_game()
		
	def count_moves(self):
		x_count, o_count = 0,0
		for row in self.board_state:
			x_count += row.count('x')
			o_count += row.count('o')
		return {'x': x_count,
				'o': o_count,
				'total': x_count + o_count}

	def determine_turn(self, of = 'player'):
		turn = 'x' if self.count_moves()['x'] == self.count_moves()['o'] else 'o' 	
		if of == 'player':
			return getattr(self, turn)
		else:
			return turn

	def sum_along_path(self, line_type, axis, mark):
		if line_type == 'row':
			return self.board_state[axis].count(mark)
		elif line_type == 'column':
			return [column[axis] for column in self.board_state].count(mark)
		elif line_type == 'diagonal':
			diagonal = lambda i, axis: self.board_state[2*(axis%2) +((-1)**axis)*i][i] 
			return [diagonal(i, axis) for i in range(3)].count(mark)

	def evaluate_game(self):
		moves = self.count_moves()['total']
		self.winner = None
		if moves == 0:
			self.game_state = None
			self.winner = None
			return None
		else:
			self.game_state = 'continue'
			if moves < 3:
				return None
			else:
				for line_type in ['diagonal','column', 'row']:
					for mark in ['x','o']:
						evaluations = [self.sum_along_path(line_type, axis, mark) for axis in range(3)]
						if 3 in evaluations: 
							self.winner = getattr(self, mark) 
							self.game_state = 'win'
							return None
				if self.count_moves()['total'] == 9:
					self.game_state = 'draw'

	###UNTESTED###
	def user_interface(self):
		'''
		This function is a single pass through the interface loop.
		Control flow for the loop is contained in the command loop
		function rather than here.
		'''

		prompt = self.prompt()			
		print(self) #Prints the board

		if self.game_state in ['draw', 'win']:
			start_new_game = self.sanitize_input(prompt, input_type='decision')
			if start_new_game:
				self.board_state = self.blank_board()
				self.evaluate_game()
				return None				
			else:
				self.quit = True
				raise Exception('q')
		else:
			user_input = self.sanitize_input(prompt, input_type='move')
			self.update_board(user_input)		
			self.evaluate_game()
			return None

	def sanitize_input(self, prompt, input_type = None):
		while True:
			user_input = input(prompt + '\n')	
			if user_input in ['q', 'r']:
				confirm = input(f'Enter {user_input} again to confirm command\n')
				if confirm == user_input: 
					self.quit = user_input == 'q'
					self.reboot = user_input =='r'
					raise Exception(user_input)

			elif user_input == 'h':
				print(self.help_string)

			elif user_input == 'b':
				print(self.blurb_string)
			
			elif input_type == 'move':
				valid_move = re.compile(r'[abc][123]')		
				matched_move = valid_move.match(user_input)
				if not matched_move:
					print('Invalid entry')
				else:
					return matched_move[0]

			elif input_type == 'decision':
				valid_decision = re.compile(r'[yn]')
				matched_decision = valid_decision.match(user_input)
				if not matched_decision:
					print('Invalid entry')
				else:
					return matched_decision[0] == 'y'

			else:
				#Also if input_type == 'names'
				return user_input	

	def prompt(self):
		switcher = {
			'win': f'Game over! {self.winner} wins! Play again?',
			'draw' : 'Looks like a draw! Play again?',
			'continue' : f'It\'s {self.determine_turn()}\'s turn! Select square.' 
		}
		return switcher.get(self.game_state, 
			f'Let the games begin! It\'s {self.determine_turn()}\'s turn! Select square.')

	def command_loop(self):
		while True:
			self.startup()
			try:
				while True:
					self.user_interface()	
			except:
				if self.quit:
					self.quit = False
					print('Thank you for playing!')
					return None	
				elif self.reboot:
					self.reboot = False
					continue	

def main():
	board = Board()
	board.command_loop()
	return None

if __name__ == '__main__':
	main()
