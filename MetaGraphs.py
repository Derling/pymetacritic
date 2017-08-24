#!/usr/bin/env python3
import matplotlib.pyplot as plt 
from metacritic import pygamecritic as pgn

CONSOLES = [ #Current generation of consoles supported on Metacritic.com
    'Playstation 4',
    'Xbox One',
    'Pc',
    'Switch',
    'Wii U',
    '3ds',
	 'Playstation Vita',
    'Ios',
    'Legacy'
]


class MetaGraphs():
    def __init__(self, game, critics=True, users=True, pool=True, reviews=False):
        self.data = []
        for console in CONSOLES: 
            try: 
                self.data.append(
                        pgn.PyGameCritic(
                                console, 
                                game.title(), 
                                critics, 
                                users, 
                                pool, 
                                reviews
                                )
                        )
            except:
                pass
        ''' add these into last set up function later'''
        self.figure, self.axes = plt.subplots(len(self.data), 2)
        self.set_up_user_graphs()
        plt.tight_layout()
        plt.suptitle(game.title())
        plt.subplots_adjust(wspace=.5, top=.9)
        plt.show()
        
    def set_up_user_graphs(self):
        self.axes[0,0].set_title('Users')
        for ax in range(len(self.data)):
            user_data = self.data[ax].user_reviews['totals']
            x, y = [], []
            for score in user_data:
                x.append(score)
                y.append(user_data[score])
            ''' change colors later '''
            self.axes[ax, 0].bar(x,y,color='red',label=self.data[ax].console)
            self.axes[ax, 0].set_xticks(range(0,11))
            y_tick_range = max(y) + 10 - max(y) % 10
            self.axes[ax, 0].set_yticks(range(0, y_tick_range, int(y_tick_range/5)))
            self.axes[ax, 0].set_xlabel('Rating', fontsize=10)
            self.axes[ax, 0].legend()
            
if __name__ == '__main__':
    t = MetaGraphs(input('Enter the game:'))
    print('***** RESULTS *****')
    for data in t.data:
        print(data)