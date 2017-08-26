#!/usr/bin/env python3
import matplotlib.pyplot as plt 
from metacritic import pygamecritic as pgn

CONSOLES = { #curent generation of consoles and their colors for graphing 
        'Playstation 4' : '#003597',
        'Xbox One' : '#00971F',
        'Pc' : '#00B2FF',
        'Switch' : '#BAFF00',
        'Wii U' : '#121900',
        '3ds' : '#FF0000',
        'Playstation Vita' : '#001C5A',
        'Ios' : '#B11D4F',
        'Legacy' : '#88008C'
    }

class MetaGraphs():
    
    def __init__(self, game, critics=True, users=True, pool=True, reviews=False):
        self.data = []
        self.game = game.title()
        self.critics = critics
        self.users = users
        self.pool = pool
        self.reviews = reviews
        self.get_data()
        self.init_graphs()
        
    def get_data(self):
        for console in CONSOLES:
            try: 
                self.data.append(
                        pgn.PyGameCritic(
                                console, 
                                self.game, 
                                self.critics, 
                                self.users, 
                                self.pool, 
                                self.reviews
                                )
                        )
            except:
                pass
    
    def init_graphs(self):
        if self.data:
            self.figure, self.axes = plt.subplots(len(self.data), 2)
            self.set_up_user_graphs()
            self.set_up_critic_graphs()
            plt.tight_layout()
            plt.suptitle(self.game)
            plt.subplots_adjust(wspace=.5, top=.9)
            plt.show()
        
    def set_up_critic_graphs(self):
        self.axes[0,1].set_title('Critics')
        for ax in range(len(self.data)):
            critic_data = self.format_critics(
                    self.data[ax].critic_reviews['totals'])
            x, y = [], []
            for score in critic_data:
                x.append(score)
                y.append(critic_data[score])
            self.axes[ax, 1].bar(x, y, color=CONSOLES[self.data[ax].console],
                     label=self.data[ax].console)
            self.axes[ax, 1].set_xticks(range(0,11))
            y_tick_range = max(y) + 10 - max(y) % 10
            self.axes[ax, 1].set_yticks(range(0, y_tick_range, 
                     int(y_tick_range/5)))
            self.axes[ax, 1].set_xlabel('Rating', fontsize=10)
            self.axes[ax, 1].legend()
    
    def set_up_user_graphs(self):
        self.axes[0,0].set_title('Users')
        for ax in range(len(self.data)):
            user_data = self.data[ax].user_reviews['totals']
            x, y = [], []
            for score in user_data:
                x.append(score)
                y.append(user_data[score])
            self.axes[ax, 0].bar(x, y, color=CONSOLES[self.data[ax].console], 
                     label=self.data[ax].console)
            self.axes[ax, 0].set_xticks(range(0,11))
            y_tick_range = max(y) + 10 - max(y) % 10
            self.axes[ax, 0].set_yticks(range(0, y_tick_range, 
                     int(y_tick_range/5)))
            self.axes[ax, 0].set_xlabel('Rating', fontsize=10)
            self.axes[ax, 0].legend()
            
    def format_critics(self,data):
        # instantiate a dictionary with keys 0-10 and values 0
        r_value = dict(zip(range(0,11), [0] * 10))
        for key in data:# make critic scores single digit. 
            r_value[int(key/10)] = r_value.get(int(key/10),0) + data[key]
        return r_value
            
if __name__ == '__main__':
    t = MetaGraphs(input('Enter the game:'))
    print('***** RESULTS *****')
    for data in t.data:
        print(data)
