#!/usr/bin/env python3
from metacritic import PyGameCritic as pgn
import logging
import matplotlib.pyplot as plt 


#Module for generating bar graphs comparing the metacritic scores of a game
#accross multiple consoles. 

#Current generation of consoles, also only ones supported on metacritic.com
CONSOLES = ['playstation-4','xbox-one','pc','switch','wii-u','3ds',
				'playstation-vita','ios','legacy']

class MetaGraphs():
    def __init__(self,game):
        self.data = []
        self.game = game
        self.find_consoles()

    def find_consoles(self):
    	for console in CONSOLES:
    		#If the game is released on a console, add the class instance to
    		#data array
    		try: 
    			tmp = pgn.PyGameCritic(console,self.game)
    			self.data.append(tmp)
    		except Exception as e:
    			#If the game is not available on a certain console, do nothing.
    			pass

if __name__ == '__main__':
	x = MetaGraphs('the witcher 3 wild hunt')  