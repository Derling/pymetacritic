from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

''' 
    Testing proved a bit buggy, after multiple tests and lots of html reviews,
    I have concluded that some of metacritics reviews get pulled from the site.
    Many of the pulled reviews are actually critic reviews, not user reviews.
    My tests have confirmed this because they always produce the correct number
    of user reviews stated on the game's metacritic summary site.
    Due to this discovery, many of the sites numbers are inaccurate. 
    ie, the fourth review for the pc version of the witcher 3 the wild hunt is
    a blank review, used as padding it seems for some reason. To test this 
    enter pc as the console and "the witcher 3 the wild hunt" as the game.
    Check the site's html here: 
    http://www.metacritic.com/game/pc/the-witcher-3-wild-hunt/critic-reviews.
    It is in plain view that the fourth list item is an empty div with the
    style of the actual reviews with content. 
    Another factor that may contribute to the site's wrong numbers is that there
    are a few reviews(mainly critic reviews) that have not been published. 
    In my script I only consider reviews that have been graded. When tested 
    against games that have no unpublished rerviews and no removed reviews, 
    script works as intended.
'''
#Turned into class for portability, readability and reuseability
#Change of scope, need to add parameter to check whether we want to pull
#full review body or not, currently we are pulling review body and not doing
#anything with it, to reduce redundancy and save resources add boolean. 
class PyGameCritic():
    def __init__(self, console, game, critics=True, users=True, pool=True):
        self.user_reviews = {}
        self.critic_reviews = {}
        self.reviews = {}
        self.get_all_metacritic_data(console, game, critics, users, pool)
        print(len(self.user_reviews),len(self.critic_reviews))
    #Main method, pool parameter used to determine whether we want all reviews 
    def get_all_metacritic_data(self, console, game, critics, users, pool): 
        url = 'http://www.metacritic.com/game/{0}/{1}' \
            .format(console.replace(' ','-'),game.replace(' ','-'))
        if critics : self.reviews['critics'] = self.get_critic_reviews(url,pool)
        if users : self.reviews['users'] = self.get_user_reviews(url,pool)

    #get user reviews
    def get_user_reviews(self, url, pool, page=0):
        req = Request(url + '/user-reviews?page=' + str(page) 
                        , headers={'User-Agent': 'Mozilla/5.0'})
        html_doc = urlopen(req).read()
        soup = BeautifulSoup(html_doc,'lxml')
        ol = soup.find_all('ol',{'class':'reviews user_reviews'})
        user_elements = 0
        if ol:
            user_elements = ol[0].find_all('li',{'class':'review user_review'})
        #If statement to check if there is at least one review
        if soup.find('li',{'class':'review user_review first_review'}) :
            f_r = self.get_special_review(soup.find('li',{'class':'review user_review first_review'}))
            self.user_reviews[f_r[0]] = {'name':f_r[1], 'review':f_r[2], 'score':f_r[3]}
        #If statement to check if there are at laest two 
        if soup.find('li',{'class':'review user_review last_review'}): 
            l_r = self.get_special_review(soup.find('li',{'class':'review user_review last_review'}))
            self.user_reviews[l_r[0]] = {'name':l_r[1], 'review':l_r[2], 'score':l_r[3]}
        #If statements to check if there is only one review
        if soup.find('li',{'class':'review user_review first_review last_review'}):
            only_review = self.parse_tag(
                    soup.find('li',{'class':'review user_review first_review last_review'}))
            self.user_reviews[only_review[0]] = {'name':only_review[1],
                        'review':only_review[2],'score':only_review[2]}
        # necessary if statement in case there are less than 3 reviews
        if user_elements: 
            for user_review in user_elements:
                data = self.parse_tag(user_review)
                self.user_reviews[user_review['id']] = {'name':data[0],
                            'review':data[1], 'score':int(data[2])}
        # if pool = 1 and there are more reviews on a different webpage:
        #         get all the user reviews for next page    
        if pool and soup.find('a', {'class':'action','rel':'next'}, href=True):
            self.get_user_reviews(url, pool, page+1)
        return self.user_reviews

    # get critic rerviews
    def get_critic_reviews(self, url, pool, page=0):
        req = Request(url + '/critic-reviews?page=' + str(page)
                      , headers={'user-Agent': 'Mozilla/5.0'})
        html_doc = urlopen(req).read()
        soup = BeautifulSoup(html_doc,'lxml')
        ol = soup.find_all('ol',{'class':'reviews critic_reviews'})
        critic_elements = 0
        if ol:
            critic_elements = ol[0].find_all('li',{'class':'review critic_review'})
            #If statement to check if there is at least one review
        if soup.find('li',{'class':'review critic_review first_review'}):
            f_r = self.get_special_review(soup.find('li',{'class':'review critic_review first_review'}), False)
            self.critic_reviews[f_r[0]] = {'review':f_r[1], 'score':f_r[2]}
        #If statement to check if there are at laest two 
        if soup.find('li',{'class':'review critic_review last_review'}):
            l_r = self.get_special_review(soup.find('li',{'class':'review critic_review last_review'}), False)
            self.critic_reviews[l_r[0]] = {'review':l_r[1], 'score':l_r[2]}
        #If statement to check if there is only one review
        if soup.find('li',{'class':'review critic_review first_review last_review'}):
            only_review = self.parse_tag(
                    soup.find('li',{'class':'review critic_review first_review last_review'}))
            self.critic_reviews[only_review[0]] = {'review':only_review[1]
                                    ,'score':only_review[2]}
        #If statement in case there are more than 2 reviews
        if critic_elements:
            for critic_review in critic_elements:
                data = self.parse_tag(critic_review)
                self.critic_reviews[data[0]] = {'review':data[1], 'score':data[2]}
        # if pool = 1 and there are more reviews on a different webpage:
        #         get all the user reviews for next page
        if pool and soup.find('a', {'class':'action','rel':'next'}, href=True):
            self.get_user_reviews(url, pool, page+1)
        return self.critic_reviews

    #extrace li element literals
    def parse_tag(self, tag_data):
        return (
                tag_data.find('a',href=True).getText(),
                tag_data.find('div',{'class':'review_body'}).getText(),
                tag_data.find('div',{'class':'metascore_w'}).getText())

    #extract first and last review 
    def get_special_review(self, tag, user=True):
        if user:
            tag_data = self.parse_tag(tag)
            return(tag['id'],tag_data[0],tag_data[1],
                   int(tag_data[2]))
        else:
            tag_data = self.parse_tag(tag)
            return(tag_data[0],tag_data[1],
                   int(tag_data[2]))

if __name__ == '__main__':
    #set pool to 1 to test if script pulls all reviews.
    try:
        PyGameCritic(input('Enter the console:').strip()
                            ,input('Enter the game:').strip().lower())
    except Exception as e:
        raise Exception(
            "Ran into an error, most likely mispelled console or game title",
            'System error :',e)