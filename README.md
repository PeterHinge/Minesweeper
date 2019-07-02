# Minesweeper
Minesweeper including AI 

Minesweeper 2.0 includes probabilistic AI
<br>Here is an article that explains how the AI works: https://luckytoilet.wordpress.com/2012/12/23/2125/

How to play:
<br>Works like normal minesweeper ('r' to restart, 'a' to enable/disable AI)

Requirements:
<br>Python 3.6
<br>PyGame 1.9

_______________________________________________________
Plan:
<br>2019-03-25: Want to create basic minesweeper program to play including having an AI to play for you.

_______________________________________________________
<br>Log:
<br>2019-03-25: Finished up minesweeper without computer play. Will program the AI tomorrow.
<br>2019-03-26: Did rule based computer play. Will clean up code tomorrow. EDIT: found a better way to do AI - will do that tomorrow.
<br>2019-03-27: Cleaned up code-base. Gonna wait with implementation of optimized AI solution till later date. 
<br>2019-05-02: Rebuild the game from scratch. Minesweeper 2.0 including a near perfect AI

_______________________________________________________
<br>Notes:
<br>2019-03-26: Realized a more optimized AI solution based on probability.
<br>2019-03-27: Realized a much smarter way of constructing core program. Instead of having an underlying table with a graphical cover, I can build the game as one cohesive class. Don't wanna rebuild the whole thing now as I believe starting from scratch is just as fast.
<br>2019-03-27: Wanna wait with the optimized AI solution till I rebuild the game. For now I'll clean up this code and then return to this project later on. 
<br>2019-05-02: One final optimization I see is to include: if remaining mines less likely than any available cell, pick the optimal cell (but this seems very difficult).
