#!/usr/bin/env python3
import re
from collections import Counter

import requests
from bs4 import BeautifulSoup

from .stopwords import STOP_WORDS


class MetaCriticParserBase:

    METACRITIC_URL = "https://www.metacritic.com"
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'


    def get_all_review_word_counts(self, users=True, critics=True):
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
        regex = '\\b\\w+\\b'
        words = []

        for word in  re.findall(regex, review):
            casefold_word = word.casefold()
            if casefold_word not in STOP_WORDS:
                words.append(casefold_word)

        return words


    def get_reviewers_word_count(self, url, reviewers, count=None, page=0):
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
        return bool(soup.find('a', {'class':'action','rel':'next'}, href=True))


    def _get_review_body(self, review_element):
        review_body = review_element.find('div', {'class': 'review_body'})

        extended_body = review_body.find('span', {'class': 'blurb blurb_expanded'})
        if bool(extended_body):
            return extended_body.getText()

        return review_body.getText()


    def get_reviewer_meta_score(self, reviewer):
        url = self.get_url()
        req = requests.get(url, headers={'User-Agent': self.USER_AGENT})
        soup = BeautifulSoup(req.text, 'lxml')

        metascore = soup.find('a', {'class': 'metascore_w'}).getText()
        return metascore



    def _update_reviewer_count(self, reviewer):
        attr = f'{reviewer}_reviews'
        setattr(self, attr, getattr(self, attr) + 1)

    def get__url(self):
        # interface method subclasses must implement
        # should return the url that gets used to make the request call
        raise NotImplemented


    def _get_reviews(soup, reviewer):
        # each media type has differing ways of posting the reviews
        # games use an ol while movies use a regular div
        # derived class has to implement this themselves
        raise NotImplemented

