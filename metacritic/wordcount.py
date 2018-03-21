#!/usr/bin/env python3
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from collections import defaultdict

'''
    import dependencies
    
    querydata contains a wrapper class for the information used to extract 
    the html source code from the web
    
    shortwords module has a set of strings, the strings are words
    which should not be considered when counting which words appear most
    
'''

try:
    # relative import
    from . import querydata as qd
    from . import stopwords as sw
except ImportError:
    try:
        # absolute import
        import querydata as qd
        import stopwords as sw
    except ModuleNotFoundError:
        raise ModuleNotFoundError # one of the dependencies not found

REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

PUNCTUATION = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

class MetaCritic():
    def __init__(self, media='', title='', platform='', critics=True, users=True, pool=True):
        self.user_words = defaultdict(int)
        self.critic_words = defaultdict(int)
        self.critics = critics
        self.users = users
        self.pool = pool
        self.query_data = qd.QueryData(media, platform, title)
        self.__get_all_metacritic_data()

    def __get_all_metacritic_data(self):
        if self.critics: 
            self.__get_reviews()
        if self.users: 
            self.__get_reviews(client='critic')
    
    def __get_reviews(self, client='user', page=0):
        url = self.get_url() + f'/{client}-reviews?page=' + str(page)
        req = Request(url, headers=REQUEST_HEADERS)
        html_doc = urlopen(req).read()
        soup = BeautifulSoup(html_doc,'lxml')
        ol = soup.find('ol', {'class':'reviews user_reviews'})

        reviews = None
        if ol:
            reviews = ol.find_all('li',{'class':'review user_review'})

        if soup.find(
             'li', {'class':'review user_review first_review last_review'}): # only one review on current page
            review_content = self.__parse_tag(soup.find(
                'li', {'class':'review user_review first_review last_review'}))
            for word in get_words(review_content):
                if word.casefold() in sw.WORDS:
                    continue
                getattr(self, f'{client}_words')[word] += 1


        if soup.find('li',{'class':'review user_review first_review'}): # get first review on current page
            review_content = self.__parse_tag(
                  soup.find('li', {'class':'review user_review first_review'}))
            for word in get_words(review_content):
                if word.casefold() in sw.WORDS:
                    continue
                getattr(self, f'{client}_words')[word] += 1
                

        if reviews: # reviews between first and last review
            for review in reviews:
                review_content = self.__parse_tag(review)
                for word in get_words(review_content):
                    if word.casefold() in sw.WORDS:
                        continue
                    getattr(self, f'{client}_words')[word] += 1
                
        if soup.find('li', {'class':'review user_review last_review'}): # get last review on current page
            review_content = self.__parse_tag(
                  soup.find('li', {'class':'review user_review last_review'}))
            for word in get_words(review_content):
                if word.casefold() in sw.WORDS:
                    continue
                getattr(self, f'{client}_words')[word] += 1

        if (self.pool and 
                soup.find('a', {'class':'action','rel':'next'}, href=True)):
            self.__get_reviews(client, page+1) # if pool recursively get all reviews from next page



    def __parse_tag(self, tag):
    	# extract the content of the review
    	return tag.find('div',{'class':'review_body'}).getText()
                
    def __repr__(self):
    	# standard __repr__ method *** Looks sloopy fix later ***
        qd = self.get_query_data()
        return f'PyGameCritic(media={qd.media}, title={qd.title}, platform={qd.platform}, ' \
               + f'critics={self.critics}, users={self.users}, pool={self.pool})'

    def get_url(self):
        # return the url being used to gather information
        return self.query_data.url
    
    def get_query_data(self):
        # return the wrapper class for storing query information
        return self.query_data


def get_words(string):
    # generator which gets all words in a string 
    # trans_table used to map punctuation marks to an empty string
    # yield the words translated using the translation table
    words = string.split()
    trans_table = str.maketrans({p: '' for p in PUNCTUATION}) 
    for word in words:
        yield word.translate(trans_table)