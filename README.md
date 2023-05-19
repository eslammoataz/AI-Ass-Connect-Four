# Connect Four AI

This project is a Connect Four game implemented in Python, where you can play against an <br>
AI opponent. The AI uses the Minimax algorithm, with an optional Alpha-Beta pruning <br>
enhancement, to decide its moves. <br>
 <br><br>
 
# Features <br>
1 - Fully functional Connect Four game, playable in a GUI. <br>
2 - AI opponent that uses the Minimax algorithm to determine its moves. <br>
3 - Option to enable Alpha-Beta pruning, to make the AI opponent more efficient. <br>
4 - Adjustable difficulty level for the AI opponent. <br>
<br>
# How to Run <br>
1 - Ensure you have Python installed. <br>
2 - Download or clone this repository. <br>
3 - Run python main.py. <br>

# Implementation Details
The Connect Four board is implemented as a 6x7 2D list. The game mechanics include <br>
adding a piece to the board, switching between players, and checking for a win.<br>

The AI opponent uses the Minimax algorithm, a decision-making algorithm used for finding <br>
the optimal move in a zero-sum game like Connect Four. This algorithm can be enhanced <br>
with Alpha-Beta pruning, which skips over branches of the game tree that don't need to be <br>
considered because they could never be chosen in an optimal play. This makes the AI more efficient. <br>

The game has a GUI, created using the pygame library. This GUI includes options for <br>
selecting the algorithm used by the AI (Minimax with or without Alpha-Beta pruning) and for <br>
setting the difficulty level of the AI opponent. <br>

We hope you enjoy playing Connect Four against this AI!
