#!/usr/bin/env python3
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from collections import namedtuple, Counter

'''
    critics field used to determine whether to pull critic data or not
    users field used to determine whether to pull user data or not

'''

MetaData = namedtuple('MetaData', ['review', 'score',])

class PyGameCritic():
    def __init__(self, console, game, critics=True, users=True, pool=True, reviews=False):
        self.user_reviews = {}
        self.critic_reviews = {}
        self.critics = critics
        self.users = users
        self.pool = pool
        self.console = console
        self.game = game
        self.reviews = reviews
        self.__get_all_metacritic_data()

    def __get_all_metacritic_data(self): 
        url = 'http://www.metacritic.com/game/{0}/{1}'.format(
                    self.console.lower().replace(' ','-'),
                    self.game.lower().replace(' ','-')
                    )
        if self.critics: 
            self.__get_critic_reviews(url)
        if self.users: 
            self.__get_user_reviews(url)
    
    def __get_user_reviews(self, url, page=0):
        req = Request(
                url + '/user-reviews?page=' + str(page),
                headers={'User-Agent': 'Mozilla/5.0'}
                )

        html_doc = urlopen(req).read()
        soup = BeautifulSoup(html_doc,'lxml')
        ol = soup.find('ol', {'class':'reviews user_reviews'})

        user_reviews = None
        if ol:
            user_reviews = ol.find_all('li',{'class':'review user_review'})

        if soup.find(
             'li', {'class':'review user_review first_review last_review'}): # only one review on current page
            name, review_data = self.__parse_tag(soup.find(
                'li', {'class':'review user_review first_review last_review'}))
            self.user_reviews[name] = {k: v for k, v in review_data._asdict().items() if v != None}


        if soup.find('li',{'class':'review user_review first_review'}): # get first review on current page
            name, review_data = self.__parse_tag(
                  soup.find('li', {'class':'review user_review first_review'}))
            self.user_reviews[name] = {k: v for k, v in review_data._asdict().items() if v != None}

        if user_reviews: # reviews between first and last review
            for user_review in user_reviews:
                name, review_data = self.__parse_tag(user_review)
                self.user_reviews[name] = {k: v for k, v in review_data._asdict().items() if v != None}

        if soup.find('li', {'class':'review user_review last_review'}): # get last review on current page
            name, review_data = self.__parse_tag(
                  soup.find('li', {'class':'review user_review last_review'}))
            self.user_reviews[name] = {k: v for k, v in review_data._asdict().items() if v != None}

        if (self.pool and 
                soup.find('a', {'class':'action','rel':'next'}, href=True)):
            self.get_user_reviews(url, page+1) # if pool recursively get all reviews from following page


    def __get_critic_reviews(self, url, page=0):
        req = Request(
                url + '/critic-reviews?page=' + str(page),
                headers={'user-Agent': 'Mozilla/5.0'}
                )
        html_doc = urlopen(req).read()
        soup = BeautifulSoup(html_doc,'lxml')
        ol = soup.find('ol',{'class':'reviews critic_reviews'})
        critic_elements = None

        if ol:
            critic_elements = ol.find_all('li', {'class':'review critic_review'})

        if soup.find(
              'li', {'class':'review critic_review first_review last_review'}): # only one review on current page
        	name, review_data = self.__parse_tag(soup.find(
        		'li', {'class':'review critic_review first_review last_review'}))
        	self.critic_reviews[name] = {k: v for k, v in review_data._asdict().items() if v != None}

        if soup.find('li',{'class':'review critic_review first_review'}): # get first review on current page
            name, review_data = self.__parse_tag(soup.find(
        		'li', {'class':'review critic_review first_review'}))
            self.critic_reviews[name] = {k: v for k, v in review_data._asdict().items() if v != None}

        
        if critic_elements: # 
            for critic_review in critic_elements:
            	name, review_data = self.__parse_tag(critic_review)
            	self.critic_reviews[name] = {k: v for k, v in review_data._asdict().items() if v}

        if soup.find('li',{'class':'review critic_review last_review'}): # get last review on current page
        	name, review_data = self.__parse_tag(soup.find(
        		'li', {'class':'review critic_review last_review'}))
        	self.critic_reviews[name] = {k: v for k, v in review_data._asdict().items() if v != None}

        
            
        if (self.pool and 
            soup.find('a', {'class':'action','rel':'next'}, href=True)):
            self.get_user_reviews(url, page+1) # recursively get all reviews
        return self.critic_reviews

    def get_user_scores(self):
    	# return the number of times the game was given a certain score by users
    	if self.users:
    		return Counter([self.user_reviews[name]['score'] for name in self.user_reviews])
    	return None

    def get_user_average(self):
    	# return the average of all the user scores
    	if self.users:
    		n = total = 0
    		for name in self.user_reviews:
    			total += int(self.user_reviews[name]['score'])
    			n += 1
    		return round(total/n, 1) # round to the tenth digit
    	return None

    def get_critic_scores(self):
    	# return the number of times the game was given a certain score by critics
    	if self.ritics:
    		return Counter([self.critic_reviews[name]['score'] for name in self.user_reviews])
    	return None

    def get_critic_average(self):
    	# return the average of all the critic scores
    	if self.critics:
    		n = total = 0
    		for name in self.critic_reviews:
    			total += int(self.critic_reviews[name]['score'])
    			n += 1
    		return round(total/n, 1) # round to the tenth digit
    	return None

    def __parse_tag(self, tag):
    	# extracts critic or user name and their review(if needed) and score
    	name = tag.find('a',href=True).getText()
    	return name, MetaData(
    		review=tag.find('div',{'class':'review_body'}).getText() if self.reviews else None,
        	score=tag.find('div',{'class':'metascore_w'}).getText(),
        )
                
    def __repr__(self):
    	# class instance representation
        return 'PyGameCritic("{0}", "{1}", critics={2},users={3}, pool={4},'\
                ' reviews={5})'.format(
                            self.console,
                            self.game,
                            self.critics,
                            self.users,
                            self.pool,
                            self.reviews
                            )
    
    def __str__(self):
        # NEED TO CREATE __str__ method
        return ''
        
if __name__ == '__main__':
    try:
        x = PyGameCritic(
                input('Enter the console:').strip(),
                input('Enter the game:').strip(), 
            	pool=False, reviews=True
                )
    except Exception as e:
        raise Exception(
            'Ran into an error, most likely mispelled console or game title',
            ' System error :',
            e
            )
