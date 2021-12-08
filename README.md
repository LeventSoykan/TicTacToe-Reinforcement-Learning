# TicTacToe-Reinforcement-Learning
## A project to create a TicTacToe player and train it to increase win/loss ratio. 

This program is inspired by the **MENACE** (Matchbox Educable Noughts and Crosses Engine) project by Donald Mitchie in 1961. I tried to build a ai-player class that trains itself while playing. <br>
With MENACE, Mitchie demonstrated an earlier version of Reinforcement Learning using matchboxes. He had 304 matchboxes, each representing a different position of tic-tac-toe board, which was also drawn on the box. <br>

The boxes contained different colors of beads, each color corresponding to a possible move(empty spots) at that position. By the first game, number of beads for each color was equal. <br>

![menace By Matthew Scroggs - Own work, CC](https://user-images.githubusercontent.com/30050029/145274379-598f4a38-b039-4ec1-aac7-de4897c53aa4.jpg)

In any position, when it is MENACE’s turn, below steps were followed:
* The Matchbox corresponding to the position is found
* A random bead is drawn from the box
* The move corresponding to the color of the bead is played
The beads are kept aside, and all positions are recorded. At the end of the game, if it is a tie, beads were returned to the box. In case of a win, extra beads were added. For losses, the bead was not returned.  <br>

Michie described his reinforcement system as "reward" and "punishment". After each game, number of beads in each color changed in favor of moves that led to a win. Which also increased the probability of random pick, being the right move.<br>

Further details could be found in below link: 
https://en.wikipedia.org/wiki/Matchbox_Educable_Noughts_and_Crosses_Engine
<br>

Here, I used numpy arrays instead of matchboxes and numeric weights instead of beads


