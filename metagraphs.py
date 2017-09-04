#!/usr/bin/env python3
import matplotlib.pyplot as plt
from metacritic import pygamecritic as pgn

CONSOLES = { # consoles on metacritic and colors for graphs
    'Playstation 4' : '#003597',
    'Xbox One' : '#00971F',
    'Pc' : '#00B2FF',
    'Switch' : '#BAFF00',
    'Wii U' : '#121900',
    '3ds' : '#FF0000',
    'Playstation Vita' : '#001C5A',
    'Ios' : '#B11D4F',
    'Legacy' : '#88008C',
    'Playstation 3': '#00246B',
    'Xbox 360' : '#004B12',
    'Psp' : '#007EB5',
    'Ds' : '#DFEDF3',
    'Xbox' : '#4A7355',
    'Playstation 2' : '#364962',
    'Gamecube' : '#67069F',
    'Game Boy Advance' : '#563A66',
    'Dreamcast' : '#57025A',
    'Nintendo 64' : '#45025A',
    'Playstaion' : '#02002E',
    }

class MetaGraphs():
    def __init__(self, game, pool=True):
        self.data = []
        self.game = game.title()
        self.pool = pool
        self.get_data()
        self.init_graphs()
        self.style_graphs()

    def get_data(self):
        for console in CONSOLES:
            try:
                self.data.append(
                    pgn.PyGameCritic(console, self.game, pool=self.pool,))
            except:
                pass

    def init_graphs(self):
        if self.data and len(self.data) > 1:
            self.figure, self.axes = plt.subplots(len(self.data), 2)
            self.set_up_user_graphs()
            self.set_up_critic_graphs()
        elif self.data and len(self.data) == 1:
            # The game is a console exclusive and requires a different figure
            self.figure, self.axes = plt.subplots(1, 2)
            self.set_up_user_graph()
            self.set_up_critic_graph()

    def set_up_user_graph(self):
        self.axes[0].set_title('Users')
        user_data = self.data[0].user_reviews['totals']
        x, y = [], []
        for score in user_data:
            x.append(score)
            y.append(user_data[score])
        self.axes[0].bar(x, y, color=CONSOLES[self.data[0].console],
                         label=self.data[0].console)
        self.axes[0].set_xticks(range(0, 11))
        y_tick_range = max(y) + 10 - max(y) % 10
        self.axes[0].set_yticks(range(0, y_tick_range,
                                      int(y_tick_range/5)))
        self.axes[0].set_xlabel('Rating', fontsize=10)
        self.axes[0].legend()

    def set_up_critic_graph(self):
        self.axes[1].set_title('Critic')
        critic_data = self.format_critics(
            self.data[0].critic_reviews['totals'])
        x, y = [], []
        for score in critic_data:
            x.append(score)
            y.append(critic_data[score])
        self.axes[1].bar(x, y, color=CONSOLES[self.data[0].console],
                         label=self.data[0].console)
        self.axes[1].set_xticks(range(0, 11))
        y_tick_range = max(y) + 10 - max(y) % 10
        self.axes[1].set_yticks(range(0, y_tick_range,
                                      int(y_tick_range/5)))
        self.axes[1].set_xlabel('Rating', fontsize=10)
        self.axes[1].legend()

    def style_graphs(self):
        plt.tight_layout()
        plt.suptitle(self.game)
        plt.subplots_adjust(hspace=.5, wspace=.5, top=.9)
        plt.show()

    def set_up_critic_graphs(self):
        self.axes[0, 1].set_title('Critics')
        for ax in range(len(self.data)):
            critic_data = self.format_critics(
                self.data[ax].critic_reviews['totals'])
            x, y = [], []
            for score in critic_data:
                x.append(score)
                y.append(critic_data[score])
            self.axes[ax, 1].bar(x, y, color=CONSOLES[self.data[ax].console],
                                 label=self.data[ax].console)
            self.axes[ax, 1].set_xticks(range(0, 11))
            y_tick_range = max(y) + 10 - max(y) % 10
            self.axes[ax, 1].set_yticks(range(0, y_tick_range,
                                              int(y_tick_range/5)))
            self.axes[ax, 1].set_xlabel('Rating', fontsize=10)
            self.axes[ax, 1].legend()

    def set_up_user_graphs(self):
        self.axes[0, 0].set_title('Users')
        for ax in range(len(self.data)):
            user_data = self.data[ax].user_reviews['totals']
            x, y = [], []
            for score in user_data:
                x.append(score)
                y.append(user_data[score])
            self.axes[ax, 0].bar(x, y, color=CONSOLES[self.data[ax].console],
                                 label=self.data[ax].console)
            self.axes[ax, 0].set_xticks(range(0, 11))
            y_tick_range = max(y) + 10 - max(y) % 10
            self.axes[ax, 0].set_yticks(range(0, y_tick_range,
                                              int(y_tick_range/5)))
            self.axes[ax, 0].set_xlabel('Rating', fontsize=10)
            self.axes[ax, 0].legend()

    def format_critics(self, data):
        # instantiate a dictionary with keys 0-10 and values 0
        r_value = dict(zip(range(0, 11), [0] * 10))
        for key in data:# make critic scores single digit.
            r_value[int(key/10)] = r_value.get(int(key/10), 0) + data[key]
        return r_value

if __name__ == '__main__':
    t = MetaGraphs(input('Enter the game:'))
    print('***** RESULTS *****')
    for data in t.data:
        print(data)
