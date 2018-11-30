from .parser_base import MetaCriticParserBase

class GameParser(MetaCriticParserBase):
	"""Metacritic parser for video games

	Args:
		platform(str): the platform the game was released on
			supported platforms(followed by their Metacritic alias):
				PS4(playstation-4),
				Xbox One(xbox-one),
				PC(pc),
				Switch(switch),
				Wii U(wii-u),
				3DS(3ds)
				PS Vita(playstation vita),
				iOS(ios),
				PS3(playstation-3),
				PS2(playstation-2),
				PS(playstation),
				Xbox 360(xbox-360),
				Xbox(xbox),
				DS(ds),
				N64(nintendo-64),
				PSP(psp),
				Wii(wii),
				Gamecube(gamecube),
				Game Boy Advance(game-boy-advance),
				Dreamcast(dreamcast)
		title(str): the title of the game
			All title must be all lowercase with whitespace replaced by "-". Read Dead Redemption 2
			should be passed in as red-dead-redemption-2

	When instantiating a GameParser object the platform should be the Metacritic alias and not
	the actual name of the platform. For example if the game was release on Xbox One, the platform
	would be xbox-one.
	"""

	def __init__(self, platform, title):
		self.platform = platform
		self.title = title


	def get_url(self):
		"""Returns the base url that will get used when making requests
		"""
		return '/'.join([self.METACRITIC_URL, 'game', f'{self.platform}', f'{self.title}'])


	def _get_reviews(self, soup, reviewer):
		"""Get all the review elements for a given html doc

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

		one_review_in_page = reviews_element.find('li', {'class':'review user_review first_review last_review'})
		if one_review_in_page:
			return [one_review_in_page]
		
		reviews = [reviews_element.find('li',{'class': f'review {reviewer}_review first_review'})]
		reviews.extend(reviews_element.find_all('li', {'class': f'review {reviewer}_review'}))
		reviews.append(reviews_element.find('li', {'class': f'review {reviewer}_review last_review'}))

		return reviews