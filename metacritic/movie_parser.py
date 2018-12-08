from .parser_base import MetaCriticParserBase

class MovieParser(MetaCriticParserBase):
	""" Metacritic parser for movies

	Args:
		movie(str): the title of the movie.
		year(int): the year the movie was released. This is an optional argument
					and should only be included to specify the version of a movie
					that has been either rebooted or released twice with the same
					name. An example of this would be The Mummy. The original version
					was released on 1999 and the reboot was released 2017. To parse data
					for the original version do not include the year. To parse the data for
					the 2017 version of The Mummy include the year 2017.
	"""

	def __init__(self, movie, year=None):
		self._movie = movie.title()
		self._metacritic_name = self.format_title_name(movie)
		self._year = year


	@property
	def movie(self):
		""" Getter method for the Movie attribute. """
		return self._movie


	@property
	def year(self):
		""" Getter method for the year attribute. """
		return _year


	def get_url(self):
		""" Returns the base url that will get used when making requests """
		return '/'.join([self.METACRITIC_URL, 'movie', f'{self._metacritic_name}-{self._year}']) if self._year \
			   else '/'.join([self.METACRITIC_URL, 'movie', f'{self._metacritic_name}'])


	def _get_review_body(self, review_element):
		""" Returns the contennt of a review element

        Args:
        	review_element(bs4.element.Tag): a bs4 element tag object

        Returns:
        	The body of a review
        """
		review_body = review_element.find('div', {'class': 'summary'})

		external_summary = review_body.find('a', {'class': 'no_hover'})
		if bool(external_summary):
			return external_summary.getText()

		extended_review = review_body.find('span', {'class': 'blurb blurb_expanded'})
		if bool(extended_review):
			return extended_review.getText()

		return review_body.getText()


	def _get_reviews(self, soup, reviewer):
		"""Get all the review elements for a given html doc

		Args:
			soup(BeautifulSoup): a BeautifulSoup object instantiated with the html doc for
				the current page we will pull the reviews from
			reviewer(str): string that tells the function who the reviews were written by(user/critic)

		Returns:
			A list of bs4.element.Tag elements that are used to denote a review in the html
		"""
		reviews_element = soup.find('div', {'class': f'{reviewer}_reviews'})

		if not reviews_element:
			return []

		top_pad_reviews = reviews_element.find_all('div', {'class': 'review pad_top1'}) or []
		btm_pad_reviews = reviews_element.find_all('div', {'class': 'review pad_btm1'}) or []
		dbl_pad_reviews = reviews_element.find_all('div', {'class': 'review pad_top1 pad_btm1'}) or []

		return top_pad_reviews + btm_pad_reviews + dbl_pad_reviews
