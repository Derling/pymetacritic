from .parser_base import MetaCriticParserBase

class TVParser(MetaCriticParserBase):
    """ Metacritic parser for tv shows

    """

    def __init__(self, show, season=1):
    	pass


    def get_url(self):
    	""" Returns the base url that will get used when making requests """
    	pass


    def _get_review_body(self, review_element):
    	""" Returns the content of a review element

    	Args:
    		review_element(bs4.element.Tag): a bs4 element tag object

    	Returns:
    		The body of a review
    	"""
    	pass


    def _get_reviews(self, soup, reviewer):
    	""" Gets all the review elements for a given html doc

    	Args:
    		soup(BeautifulSoup): a BeautifulSoup object instantiated with the html doc for
    			the current page we will pull the reviews from
    		reviewer(str): string that tells the function who the reviews were written by(user/critic)

    	Returns:
    		A list of bs4.element.Tag elements that are used to denote a review in the html
    	"""
    	pass
