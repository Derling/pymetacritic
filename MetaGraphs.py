#!/usr/bin/env python3
from metacritic import PyGameCritic as pgn
import logging
import matplotlib.pyplot as plt 


#Module for generating bar graphs comparing the metacritic scores of a game
#accross multiple consoles. 

#Current generation of consoles, also only ones supported on metacritic.com
CONSOLES = ['Playstation 4','Xbox One','Pc','Switch','Wii U','3ds',
				'Playstation Vita','Ios','Legacy']

class MetaGraphs():
    def __init__(self, game, critics=True, users=True, pool=True, reviews=False):
        self.data = []
        for console in CONSOLES:
            #If the game is released on a console, add the class instance to
            #data array
            try: 
                print('trying ...',console)
                self.data.append(pgn.PyGameCritic(console, game.title(), critics, users, pool, 
                                    reviews))
                print('success for ...',console)
            except Exception as e:
                #If the game is not available on a certain console, do nothing.
                print('failed for ...',console)
                pass

if __name__ == '__main__':
    t = MetaGraphs(input('Enter the game:'))
    print('***** RESULTS *****')
    for data in t.data:
        print(data)