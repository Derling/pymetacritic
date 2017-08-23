#!/usr/bin/env python3
from metacritic import PyGameCritic as pgn
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
            #If the game was released on a console, add the class instance to
            #data array
            try: 
                self.data.append(pgn.PyGameCritic(console, game.title(), 
                                        critics, users, pool, reviews))
            except Exception as e:
                #If the game is not available on a certain console, do nothing.
                pass
        self.figure, self.axes = plt.subplots(len(self.data),2)
        self.set_up_user_graphs()
        plt.show()
        
    def set_up_user_graphs(self):
        for ax in range(len(self.data)):
            user_data = self.data[ax].user_reviews['totals']
            x, y = [], []
            for score in user_data:
                x.append(score)
                y.append(user_data[score])
            self.axes[ax, 0].bar(x,y)
            # x axis 0-10 for all possible ratings.
            self.axes[ax, 0].set_xticks(range(0,11))
            #make y-axis 5 ticks for neater look AND for range use highest y
            #value and get next integer that is divisible by 10, ie if max is 
            #78 next int divisible by 10 is 80
            y_tick_range = max(y) + 10 - max(y) % 10
            self.axes[ax, 0].set_yticks(range(0, y_tick_range, int(y_tick_range/5)))
            
            
if __name__ == '__main__':
    t = MetaGraphs(input('Enter the game:'))
    print('***** RESULTS *****')
    for data in t.data:
        print(data)