import numpy as np
from player_module import AIPlayer,Player,RandomPlayer,HumanPlayer
import sys
import pickle

class Game:
    """
    Game Module creating the board, prompting the user to play and changing turns
    """
    def __init__(self, player1, player2, display=True, board=None):
        self.player1 = player1
        self.player2 = player2
        self.display = display
        if board is None:
            self.board = np.full((3,3),9)
        else:
            self.board = board
        self.turn = 'Player1'
        self.sign = 'X'
        self.winner = -1


    def show_board(self):
        def transform_cell(n):
            if n == 1:
                return 'X'
            elif n == 0:
                return 'O'
            return '___'
        board_tm = [transform_cell(n) for n in self.board.flatten()]
        print(f'{self.turn} move! Your sign is {self.sign}\n')
        i = 0
        for n in board_tm:
            if i==0 or i==3 or i==6:
                print(f'\n{n}\t\t', end=' ')
            else:
                print(f'{n}\t\t', end=' ')
            i += 1

    def get_selection(self):
        if self.turn=='Player1':
            s=self.player1.select_cell(self.board.flatten())
            self.board[s]=1
        else:
            s=self.player2.select_cell(self.board.flatten())
            self.board[s]=0
        self.toggle_turn()

    def toggle_turn(self):
        if self.turn == 'Player1':
            self.turn = 'Player2'
        else:
            self.turn = 'Player1'

    def play(self):
        """Starts the game and continues until one side wins
            Board display is optional.
        """
        while not self.game_finished():
            if self.display:
                self.show_board()
            self.get_selection()
        return self.winner

    def game_finished(self):
        ##Check whether any player has won/ or it is a tie. Run after each move.
        control_array = np.hstack([np.sum(self.board, axis=1), np.sum(self.board, axis=0)])
        control_array = np.append(control_array, [np.sum(np.diag(self.board)), np.sum(np.diag(np.fliplr(self.board)))])
        if 0 in control_array:
            if self.display:
                print(f'Winner is {self.player2.name}')
            self.winner=2
            if type(self.player2) == AIPlayer:
                self.player2.process_win()
            return True
        elif 3 in control_array:
            if self.display:
                print(f'Winner is {self.player1.name}')
            self.winner=1
            if type(self.player1)==AIPlayer:
                self.player1.process_win()
            return True
        elif 9 not in self.board:
            if self.display:
                print('It is a tie')
            if type(self.player1)==AIPlayer:
                self.player1.process_tie()
            if type(self.player2)==AIPlayer:
                self.player2.process_tie()
            return True
        return False

if __name__ == '__main__':
    # Load and test pre-trained player for 4 games
    with open('trained_player2.pkl', 'rb') as file:
        ai_player = pickle.load(file)
    human_player = HumanPlayer('YourName')
    for i in range(4):
        if i % 2== 0:
            game = Game(ai_player, human_player, display=True)
            game.play()
        else:
            game = Game(human_player, ai_player, display=True)
            game.play()
