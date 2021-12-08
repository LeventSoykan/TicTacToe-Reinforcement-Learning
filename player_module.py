import random
import numpy as np
from itertools import permutations

class Player:
    """
    Module for creating a TicTacToe player with a name
    and repr function. There is no selection for 'X'-'0' as main objective of this project
    is to train the AIPlayer for increased performance
    """
    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return f'Player {self.name}'


class RandomPlayer(Player):
    """This player selects a random cell from available options. It is used for training the AIPlayer"""
    def __init__(self, name):
        super(RandomPlayer, self).__init__(name=name)

    def select_cell(self, position):
        #Method for random selection of next move, depending on available moves.
        available = [i[0] for i in enumerate(position) if i[1]==9]
        selection = random.choice(available)
        return selection//3, selection%3

class HumanPlayer(Player):
    """This is a player we can control in the game. As the game shows the display, we can make a selection
    Selection is made with indexing with a comma. ex: 1,1 for middle cell or 0.0 for top left cell"""
    def __init__(self, name):
        super(HumanPlayer, self).__init__(name=name)

    def select_cell(self, position):
        #Method for user to apply selection
        val = -1
        count = 0
        move = (-1,-1)
        while val!=9:
            if count !=0:
                print('invalid selection')
            print()
            move = input(f"{self.name}'s Move: ").split(',')
            try:
                val = position[(int(move[0])*3+int(move[1]))]
            except IndexError as e:
                print('Please select available indexes 0-2')
                continue
            except ValueError as v:
                print('Please select a number')
                continue
            count += 1
        return int(move[0]), int(move[1])

class AIPlayer(Player):
    """
    The AI Player class to train. All positions are initialized with weights
    and updated with each game depending on game result.
    """
    def __init__(self,name, positions=None):
        super(AIPlayer, self).__init__(name=name)
        if positions:
            self.positions=positions
        else:
            self.positions=AIPlayer.get_positions()

        self.tie = self.positions.copy()
        self.win = self.positions.copy()

        self.selection_list = []

    def select_cell(self, pos):
        """
        Here the position is selected from positions dict
        Move is selected depending on the weights (numpy.random.choice)
        Weight of the selected move in position is:
        **Decreased by 3 if final result is a loss,
        **Increased by 2 if final result is a win,
        **Remains unchanged if it is a tie
        """

        position = tuple(pos)
        #If it is starting position, save all position weights in tie/win variables
        if position.count(9)>=8:
            self.tie = self.positions.copy()
            self.win = self.positions.copy()

        vals = np.array(self.positions[position])
        weights = vals/vals.sum()

        selection=np.random.choice(list(range(0,9)),1,False,weights)[0]
        vals[selection] += 2
        self.win[position] = vals.copy().tolist()
        n=np.maximum(vals[selection]-5,0)
        vals[selection]=n
        if vals.sum() == 0:
            vals[selection] = 1

        self.positions[position]=vals.copy().tolist()

        return selection//3, selection % 3

    @staticmethod
    def is_valid(pos):
        """This check is to remove the final positions(win_lose_tie)"""
        board= np.array(pos).reshape((3,3))
        control_array=np.hstack([np.sum(board,axis=1),np.sum(board,axis=0)])
        control_array=np.append(control_array,[np.sum(np.diag(board)),np.sum(np.diag(np.fliplr(board)))])
        return 0 not in control_array and 3 not in control_array and 9 in board

    @staticmethod
    def get_positions():
        """
        This is a method to initialize a position for each table where available slots are noted by 9.
        Then for each position, we initialize weights for available moves as 20.
        AI Player will decide next move, using these weights as probability.
        """
        positions=[]
        for i in range(5):
            for j in range(5):
                if (i-j)<2 and i>=j:
                    x_list=np.array([1 for _ in range(i)])
                    o_list=np.array([0 for _ in range(j)])
                    nines=np.full(9-len(x_list)-len(o_list),9)
                    position=np.hstack([nines,x_list,o_list])
                    positions.extend([p for p in set(permutations(position))])
        position_dict={}
        for p in positions:
            if AIPlayer.is_valid(p):
                position_dict[p]=[20 if x==9 else 0 for x in p]
                position_dict[p]=[20 if x==9 else 0 for x in p]
        return position_dict

    def process_tie(self):
        self.positions=self.tie.copy()

    def process_win(self):
        self.positions=self.win.copy()


if __name__ == '__main__':
    #Create an ai-player and show a few positions&weights
    ai = AIPlayer('ai')
    i = 0
    for key,value in ai.positions.items():
        i+=1
        if i>5:
            break
        print(f'{key}:{value}')












