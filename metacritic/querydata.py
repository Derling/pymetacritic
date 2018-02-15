BASE_URL = 'http://www.metacritic.com'


def _format_url(*args):
	# format url components to fit the metacritic endpoints
	# i.e http://www.metacritic.com/game/playstation-4/bloodborne
	return '/'.join(iter(args)).replace(' ', '-')

class QueryData:

	def __init__(self, media, platform, title):
		# store parameters and generate url
		self.media = media
		self.platform = platform
		self.title = title
		self.url = _format_url(BASE_URL, media, platform, title)

	def __repr__(self):
		# standard __repr__ function
		return f'QueryData({self.media}, {self.title}, {self.platform})'