import unittest
from unittest.mock import patch

class TestTicTac(unittest.TestCase):
	def setUp(self):
		self.board0 = Board(users = ['Nathan', 'Big Guy'],
						    board_state = [['o', 'o', 'x'],
						   				  ['x', 'o', 'x'],
										  ['x', ' ', 'o']])

		self.board1 = Board(users = ['Nathan', 'Big Guy'],
						    board_state = [['x', 'o', 'x'],
						   				  ['x', 'o', 'o'],
										  ['x', ' ', ' ']])

		self.board2 = Board(users = ['Nathan', 'Big Guy'],
						    board_state = [['x', 'o', 'x'],
						   	  			  ['x', 'o', 'o'],
										  ['o', 'x', 'x']])

		self.board3 = Board(users = ['Nathan', 'Big Guy'],
						   board_state = [['x', 'o', 'x'],
						   				  ['o', 'x', 'o'],
										  ['x', ' ', ' ']])

		self.board4 = Board(users = ['Nathan', 'Big Guy'])



	@patch('builtins.input', side_effect = ['Nathan', 'Big Guy',
								'b2', 'a2', 'a1', 'b1', 'c3',
								'n'])
	def test_command_loop(self, mock_input):
		board = Board()
		board.command_loop()
		self.assertEqual(board.winner, board.x, 'Board winner should be x')
		self.assertEqual(board.board_state[2][2], 'x', 'Lower left corner should be x')
		self.assertEqual(board.game_state, 'win')
		self.assertEqual(board.quit, False, 'self.quit should be reset to false') 

	@patch('builtins.input', side_effect = ['b2', 'a2', 'a1', 'b1', 'c3'])
	def test_user_interface(self, mock_input):
		board = self.board4
		board.user_interface()
		self.assertEqual(board.board_state[1][1], 'x', 'Center square should be x')
		self.assertEqual(board.winner, None, 'Winner value should be defined as None')
		self.assertEqual(board.game_state, 'continue')
		for i in range(4):
			board.user_interface()	
		self.assertEqual(board.board_state[2][2], 'x')
		self.assertEqual(board.winner, 'Nathan')
		self.assertEqual(board.game_state, 'win')

	@patch('builtins.input', side_effect = ['Nathan', 'Big Guy'])
	def test_startup(self, mock_input):
		board = Board()	
		board.startup()
		self.assertEqual(board.board_state, board.blank_board())	
		self.assertTrue((board.x, board.o == ('Nathan', 'Big Guy')) or (board.x, board.o == ('Big Guy', 'Nathan')))
		
	@patch('builtins.input', side_effect = ['q', 'q'])
	def test_startup_command_q(self, mock_input):
		board = Board()	
		try:
			board.startup()
			self.assertEqual(True, False, 'Did not throw exception')
		except:
			self.assertEqual(board.quit, True, 'Should set quit attribute to True')

	@patch('builtins.input', side_effect = ['r', 'r'])
	def test_startup_command_r(self, mock_input):
		board = Board()	
		try:
			board.startup()
			self.assertEqual(True, False, 'Did not throw exception')
		except:
			self.assertEqual(board.reboot, True, 'Should set reboot attribute to True')

	@patch('builtins.input',  side_effect = ['q', 'q'])
	def test_sanitize_q(self, mock_input):
		board = self.board4
		prompt = board.prompt()
		try:
			board.sanitize_input(prompt)
			self.assertEqual(True, False, 'Command Exception not raised')
		except Exception: 
			self.assertEqual(board.quit, True, 'Exception raised but quit value not set')
	
	@patch('builtins.input',  side_effect = ['r', 'r'])
	def test_sanitize_r(self, mock_input):
		board = self.board4
		prompt = board.prompt()
		try:
			board.sanitize_input(prompt)
			self.assertEqual(True, False, 'Command Exception not raised')
		except Exception: 
			self.assertEqual(board.reboot, True, 'Exception raised but reboot value not set')


	@patch('builtins.input', side_effect = ['b1', 'a1', 'fuckup', 'a2'])
	def test_sanitize_moves(self, mock_input):
		board = self.board4; prompt = board.prompt()
		for mv in ['b1', 'a1', 'a2']:
			self.assertEqual(board.sanitize_input(prompt, input_type = 'move'), mv)
		
	@patch('builtins.input', side_effect = ['y', 'fuckup', 'n'])
	def test_sanitize_decisions(self, mock_input):
		board = self.board4; prompt = board.prompt()
		self.assertEqual(board.sanitize_input(prompt, input_type = 'decision'), True)
		self.assertEqual(board.sanitize_input(prompt, input_type = 'decision'), False)

	@patch('builtins.input', return_value = 'Nathan') 
	def test_sanitize_names(self, mock_input):
		board = self.board4; prompt = board.prompt()
		self.assertEqual(board.sanitize_input(prompt, input_type = 'names'), 'Nathan')

	def test_prompt(self):
		board = self.board2
		self.assertEqual(board.prompt(), 'Looks like a draw! Play again?')
		board = self.board3
		self.assertEqual(board.prompt(), 'Game over! Nathan wins! Play again?')
		board = self.board4
		self.assertEqual(board.prompt(), 'Let the games begin! It\'s Nathan\'s turn! Select square.')

	def test_update_board(self):
		board = self.board3
		board.update_board('b3')
		self.assertEqual(board.board_state[2][1], 'o')
		board.update_board('a2')
		self.assertEqual(board.board_state[0][1], 'o')

	def test_determine_turn(self):
		self.assertEqual(self.board0.determine_turn(of = 'player'), self.board0.x)
		self.assertEqual(self.board0.determine_turn(), self.board0.x)
		self.assertEqual(self.board0.determine_turn(of = 'mark'), 'x')
		
		self.assertEqual(self.board1.determine_turn(of = 'player'), self.board1.o)
		self.assertEqual(self.board1.determine_turn(), self.board1.o)
		self.assertEqual(self.board1.determine_turn(of = 'mark'), 'o')

		
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

