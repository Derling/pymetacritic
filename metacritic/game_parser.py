from .parser_base import MetaCriticParserBase

class GameParser(MetaCriticParserBase):
	# a map for the supported platforms and their metacritic alias
	PLATFORMS = {
		'PS4': 'playstation-4',
		'Xbox One': 'xbox-one',
		'PC': 'pc',
		'Switch': 'switch',
		'Wii U': 'wii-u',
		'3DS': '3ds',
		'PS Vita': 'playstation-vita',
		'iOS': 'ios',
		'PS3': 'playstation-3',
		'PS2': 'playstation-2',
		'PS': 'playstation',
		'Xbox 360': 'xbox-360',
		'Xbox': 'xbox',
		'DS': 'ds',
		'N64': 'nintendo-64',
		'PSP': 'psp',
		'Wii': 'wii',
		'Gamecube': 'gamecube',
		'Game Boy Advance': 'game-boy-advance',
		'Dreamcast': 'dreamcast',

	}
	""" Metacritic parser for video games

	Args:
		platform(str): the platform the game was released on
		game(str): the title of the game
	"""

	def __init__(self, platform, game):
		self._platform = platform.title()
		self._metacritic_platform = self.PLATFORMS[platform] # TODO raise exception if unsopported platform is given
		self._game = game.title()
		self._metacritic_name = self.format_title_name(game)


	@property
	def platform(self):
		""" Getter method for the platform attribute. """
		return self._platform

	
	@property
	def game(self):
		""" Getter method for the game attribute. """
		return self._game


	def get_url(self):
		""" Returns the base url that will get used when making requests """
		return '/'.join([self.METACRITIC_URL, 'game', f'{self._metacritic_platform}', f'{self._metacritic_name}'])


	def _get_review_body(self, review_element):
		""" Returns the content of a review element

		Args:
			review_element(bs4.element.Tag): a bs4 element tag object

		Returns:
			The body of a review
		"""
		review_body = review_element.find('div', {'class': 'review_body'})

		extended_body = review_body.find('span', {'class': 'blurb blurb_expanded'})
		if bool(extended_body):
			return extended_body.getText()

		return review_body.getText()

	def _get_reviews(self, soup, reviewer):
		""" Get all the review elements for a given html doc

		Args:
			soup(BeautifulSoup): a BeautifulSoup object instantiated with the html doc for
				the current page we will pull the reviews from
			reviewer(str): string that tells the function who the reviews were written by(user/critic)

		Returns:
			A list of bs4.element.Tag elements that are used to denote a review in the html
		"""
		reviews_element = soup.find('ol', {'class': f'reviews {reviewer}_reviews'})

		if not reviews_element:
			return []

		one_review_in_page = reviews_element.find('li', {'class': f'review {reviewer}_review first_review last_review'})
		if one_review_in_page:
			return [one_review_in_page]
		
		reviews = [reviews_element.find('li',{'class': f'review {reviewer}_review first_review'})]
		reviews.extend(reviews_element.find_all('li', {'class': f'review {reviewer}_review'}))
		reviews.append(reviews_element.find('li', {'class': f'review {reviewer}_review last_review'}))

		return reviews
