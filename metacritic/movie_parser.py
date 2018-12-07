from .parser_base import MetaCriticParserBase

class MovieParser(MetaCriticParserBase):
	"""Metacritic parser for movies

	Args:
		movie(str): the title of the movie. All movie titles must be all lowercase 
				with whitespace replaced by "-". For example, The Mummy should come in as the-mummy.
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


	@movie.setter
	def movie(self, new_movie):
		""" Setter method for the movie attribute. """
		self._movie = new_movie.title()
		self._metacritic_name = self.format_title_name(new_movie)

	@property
	def year(self):
		""" Getter method for the year attribute. """
		return _year


	@year.setter
	def year(self, new_year):
		""" Setter method for the year attribute. """
		self._year = new_year

	def get_url(self):
		""" Returns the base url that will get used when making requests """
		return '/'.join([self.METACRITIC_URL, 'movie', f'{self._metacritic_name}-{self._year}']) if self._year \
			   else '/'.join([self.METACRITIC_URL, 'movie', f'{self._metacritic_name}'])


	def _get_reviews(self, soup, reviewer):
		"""Get all the review elements for a given html doc

		Args:
			soup(BeautifulSoup): a BeautifulSoup object instantiated with the html doc for
				the current page we will pull the reviews from
			reviewer(str): string that tells the function who the reviews were written by(user/critic)

		Returns:
			A list of bs4.element.Tag elements that are used to denote a review in the html
		"""
		pass