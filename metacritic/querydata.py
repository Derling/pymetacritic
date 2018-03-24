BASE_URL = 'http://www.metacritic.com'

class QueryData:
    # helper class for holding information about the item being looked up
    def __init__(self, media, platform, title):
        # store parameters and generate url
        self.user_review = 0
        self.critic_reviews = 0
        self.media = media
        self.platform = platform
        self.title = title
        self.url = format_url(BASE_URL, media, platform, title)

    def __repr__(self):
        # standard __repr__ function
        return f'QueryData({self.media}, {self.platform}, {self.title})'

def format_url(*args):
	# format url components to fit the metacritic endpoints
	# i.e http://www.metacritic.com/game/playstation-4/bloodborne
	return '/'.join([arg for arg in iter(args) if arg]).replace(' ', '-')