#!/usr/bin/env python3
import re
from collections import Counter

import requests
from bs4 import BeautifulSoup

from .stopwords import STOP_WORDS


class MetaCriticParserBase:
    """ Base Metacritic Parser class

    This class should never be instantiated, it should be used to derive new classes

    Args: 
        METACRITIC_URL(str): metacritic host url
        USER_AGENT(str): user agent string that is passed when making a request to the metacritic server
        user_reviews(int): the number of user reviews that have been processed
        critic_reviews(int): the number of critic reviews that have been processed
    """

    METACRITIC_URL = "https://www.metacritic.com"
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'

    def __init__(self):
        self.user_reviews = 0
        self.critic_reviews = 0

    def get_all_review_word_counts(self, users=True, critics=True):
        """ Retrieves all the words that get used by reviewers for an article on Metacritic

        Args:
            users(boolean): A flag used to determine whether or not user review data should get parsed
            critics(boolean): A flag used to determine whether or not critic review data should get parsed

        Returns:
            A dictionary with data about the most commonly used words for an article on Metacritic
        """
        self.user_reviews = 0
        self.critic_reviews = 0
        url = self.get_url()
        word_counts = {}

        if users:
            word_counts['user_counts'] = self.get_reviewers_word_count(url, 'user')
            word_counts['user_reviews'] = self.user_reviews

        if critics:
            word_counts['critic_counts'] = self.get_reviewers_word_count(url, 'critic')
            word_counts['critic_reviews'] = self.critic_reviews

        return word_counts


    def get_words(self, review):
        """ Retrieve an array of words used in the body of a review(drops common stop words)

        Args:
            review(str): the body of a review posted by a user on Metacritic

        Return:
            A list of words that were used in the review

        """
        regex = '\\b\\w+\\b'
        words = []

        for word in  re.findall(regex, review):
            casefold_word = word.casefold()
            if casefold_word not in STOP_WORDS:
                words.append(casefold_word)

        return words


    def get_reviewers_word_count(self, url, reviewers, count=None, page=0):
        """ Recursively get the word count for a reviewer type

        Args:
            url(str): the url of the Metacritic article
            reviewers(str): the reviewer type we want to parse(can either be user or critic)
            count(collections.Counter) a Counter object denoting the current count of words
            page(int): an integer to determine the page to parse on the website

        Returns:
            A collections.Counter object that determines the number of times a word
            got used to describe a Metacritic article
        """
        count = count or Counter()
        req = requests.get(url + f'/{reviewers}-reviews?page={page}', headers={'User-Agent': self.USER_AGENT})
        soup = BeautifulSoup(req.text, 'lxml')

        for review in self._get_reviews(soup, reviewers):
            review_body = self._get_review_body(review)
            words = self.get_words(review_body)
            count.update(words)
            self._update_reviewer_count(reviewers)


        if self._page_has_more_reviews(soup):
            return self.get_reviewers_word_count(url, reviewers,count, page + 1)

        return count


    def _page_has_more_reviews(self, soup):
        """ Determines whether or not the given html Metacritic doc links to another page with more reviews

        Args:
            soup(BeautifulSoup): a BeautifulSoup object that has been initialized with an html doc from Metacritic

        Returns:
            A boolean that determines whether or not there are more pages associated with the current html doc
        """
        return bool(soup.find('a', {'class':'action','rel':'next'}, href=True))


    def _update_reviewer_count(self, reviewer):
        """ Updates the number of reviews processed for users or critics

        Args:
            reviewer(str): the reviewer count to update
        """
        attr = f'{reviewer}_reviews'
        setattr(self, attr, getattr(self, attr) + 1)


    @staticmethod
    def format_title_name(title):
        """ Formats the title of an article 

        Args:
            title(str): the name of the article

        Returns:
            A string which can be used as part of the url to make a request
        """
        return title.replace(' ', '-').replace(':', '').lower()


    def _get_review_body(self, review_element):
        """ Interface method derived classes must implement.

        This method should parse a extract the contents of a review from a BS4 element tag
        """
        raise NotImplemented

    def get__url(self):
        """ Interface method derived classes must implement.

        Should return the url that will get used to make the request
        """
        raise NotImplemented


    def _get_reviews(soup, reviewer):
        """ Interface method derived classes must implement.

        Each media type has differing ways of posting the reviewes, ie
        games use an ol while movies use a regular div. Derived classes must
        overwrite this method with the correct way of getting the review elements.
        """
        raise NotImplemented

