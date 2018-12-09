from .parser_base import MetaCriticParserBase

class TVParser(MetaCriticParserBase):
    """ Metacritic parser for tv shows

    """

    def __init__(self, show, season=1):
        self._show = show.title()
        self._metacritic_name = self.format_title_name(show)
        self._season = season


    @property
    def show(self):
        return self._show


    @property
    def season(self):
        return self._season

    def get_url(self):
    	""" Returns the base url that will get used when making requests """
    	return '/'.join([self.METACRITIC_URL, 'tv', self._metacritic_name, f'season-{self._season}'])


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
