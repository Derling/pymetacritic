#!/usr/bin/env python3
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from collections import namedtuple, Counter


MetaData = namedtuple('MetaData', ['review', 'score',])

BASE_URL = 'http://www.metacritic.com'

REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

class MetaCritic():
    def __init__(self, media='', title='', platform='', critics=True, users=True, pool=True, reviews=False):
        self.user_reviews = {}
        self.critic_reviews = {}
        self.critics = critics
        self.users = users
        self.pool = pool
        self.query_data = QueryData(media, platform, title)
        self.reviews = reviews
        self.__get_all_metacritic_data()

    def __get_all_metacritic_data(self):
        if self.critics: 
            self.__get_critic_reviews()
        if self.users: 
            self.__get_user_reviews()
    
    def __get_user_reviews(self, page=0):
        req = Request(self.get_url() + '/user-reviews?page=' + str(page),
                headers=REQUEST_HEADERS)
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
            self.__get_user_reviews(page+1) # if pool recursively get all reviews from next page


    def __get_critic_reviews(self, page=0):
        req = Request(self.get_url() + '/critic-reviews?page=' + str(page),
                headers=REQUEST_HEADERS)
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

        
        if critic_elements: # more than 2 reviews
            for critic_review in critic_elements:
            	name, review_data = self.__parse_tag(critic_review)
            	self.critic_reviews[name] = {k: v for k, v in review_data._asdict().items() if v}

        if soup.find('li',{'class':'review critic_review last_review'}): # get last review on current page
        	name, review_data = self.__parse_tag(soup.find(
        		'li', {'class':'review critic_review last_review'}))
        	self.critic_reviews[name] = {k: v for k, v in review_data._asdict().items() if v != None}
            
        if (self.pool and 
            soup.find('a', {'class':'action','rel':'next'}, href=True)):
            self.__get_user_reviews(page+1) # if pool recursively get all reviews from next page

    def __parse_tag(self, tag):
    	# extracts critic or user name and their review(if needed) and score
    	name = tag.find('a',href=True).getText()
    	return name, MetaData(
    		review=tag.find('div',{'class':'review_body'}).getText() if self.reviews else None,
        	score=tag.find('div',{'class':'metascore_w'}).getText(),
        )
                
    def __repr__(self):
    	# standard __repr__ method *** Looks sloopy fix later ***
        qd = self.get_query_data()
        return f'PyGameCritic(media={qd.media}, title={qd.title}, platform={qd.platform}, ' \
               + f'critics={self.critics}, users={self.users}, pool={self.pool}, reviews={self.reviews}'
    
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
        if self.critics:
            return Counter([self.critic_reviews[name]['score'] for name in self.critic_reviews])
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

    def get_url(self):
        # return the url being used to gather information
        return self.query_data.url
    
    def get_query_data(self):
        # return the wrapper class for storing query information
        return self.query_data


def _format_url(*args):
	# format url components to fit the metacritic endpoints
	# i.e http://www.metacritic.com/game/playstation-4/bloodborne
	return '/'.join(iter(args)).replace(' ', '-')

class QueryData:
    # helper class for holding information about the item being looked up
	def __init__(self, media, platform, title):
		# store parameters and generate url
		self.media = media
		self.platform = platform
		self.title = title
		self.url = _format_url(BASE_URL, media, platform, title)

	def __repr__(self):
		# standard __repr__ function
		return f'QueryData({self.media}, {self.platform}, {self.title})'