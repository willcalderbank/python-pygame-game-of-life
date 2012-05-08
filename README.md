python-pygame-game-of-life
==========================

Another silly little program, the game of life implemenet with pygame. This is what happens when you have a boring afternoon. 

Its pretty straight foward although deminstates really well how expensive it is for pygame to draw to the screen (blit-ting). Really hacked together, taking the screen size as the size of the grid then splitting it up based on the stated size of each cell, to form a grid this grid is where the game of life is played out.

The speed can be controlled by only running update grid every X millseconds. 

Cells can be set to true (born/created/ect) by clicking, holding the mouse button down allows multiple cells to be set per generation.