from .parser_base import MetaCriticParserBase

class GameParser(MetaCriticParserBase):

	def __init__(self, platform, title):
		self.platform = platform
		self.title = title


	def get_url(self):
		return '/'.join([self.METACRITIC_URL, 'game', f'{self.platform}', f'{self.title}'])


	def _get_reviews(self, soup, reviewer):
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