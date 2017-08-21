#!/usr/bin/env python3
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
    
    def __init__(self, console, game, critics=True, users=True, pool=True, reviews=False):
        self.user_reviews = {}
        self.critic_reviews = {}
        self.critics = critics
        self.users = users
        self.pool = pool
        self.console = console.lower()
        self.game = game.lower()
        self.reviews = reviews
        self.get_all_metacritic_data()
        self.calculateAvgs()
        self.userTotals()
        self.criticTotals()
        
    #Main method, pool parameter used to determine whether we want all reviews 
    def get_all_metacritic_data(self): 
        url = 'http://www.metacritic.com/game/{0}/{1}' \
            .format(self.console.replace(' ','-'),self.game.replace(' ','-'))
        if self.critics : self.get_critic_reviews(url)
        if self.users : self.get_user_reviews(url)

    #get user reviews
    def get_user_reviews(self, url, page=0):
        req = Request(url + '/user-reviews?page=' + str(page) 
                        , headers={'User-Agent': 'Mozilla/5.0'})
        html_doc = urlopen(req).read()
        soup = BeautifulSoup(html_doc,'lxml')
        ol = soup.find('ol',{'class':'reviews user_reviews'})
        user_elements = 0
        if ol:
            user_elements = ol.find_all('li',{'class':'review user_review'})
        #If statement to check if there is at least one review
        if soup.find('li',{'class':'review user_review first_review'}) :
            f_r = self.get_special_review(soup.find('li',{'class':'review user_review first_review'}))
            if self.reviews:
                self.user_reviews[f_r[0]] = {'name':f_r[1], 'review':f_r[2], 'score':f_r[3]}
            else :
                self.user_reviews[f_r[0]] = {'name':f_r[1], 'score':f_r[2]}
        #If statement to check if there are at laest two 
        if soup.find('li',{'class':'review user_review last_review'}): 
            l_r = self.get_special_review(soup.find('li',{'class':'review user_review last_review'}))
            if self.reviews:
                self.user_reviews[l_r[0]] = {'name':l_r[1], 'review':l_r[2], 'score':l_r[3]}
            else:
                self.user_reviews[l_r[0]] = {'name':l_r[1], 'score':l_r[2]}
        #If statements to check if there is only one review
        elif soup.find('li',{'class':'review user_review first_review last_review'}):
            only_review = self.parse_tag(
                    soup.find('li',{'class':'review user_review first_review last_review'}))
            if self.reviews:
                self.user_reviews[only_review[0]] = {'name':only_review[1],
                         'review':only_review[2],'score':only_review[3]}
            else:
                self.user_reviews[only_review[0]] = {'name':only_review[1],
                                     'score':only_review[2]}
        # necessary if statement in case there are less than 3 reviews
        if user_elements: 
            for user_review in user_elements:
                data = self.parse_tag(user_review)
                if self.reviews:
                    self.user_reviews[user_review['id']] = {'name':data[0],
                                'review':data[1], 'score':int(data[2])}
                else:
                    self.user_reviews[user_review['id']] = {'name':data[0],
                                     'score':int(data[1])}
        # if pool = 1 and there are more reviews on a different webpage:
        #         get all the user reviews for next page    
        if self.pool and soup.find('a', {'class':'action','rel':'next'}, href=True):
            self.get_user_reviews(url, page+1)
        return self.user_reviews

    # get critic rerviews
    def get_critic_reviews(self, url, page=0):
        req = Request(url + '/critic-reviews?page=' + str(page)
                      , headers={'user-Agent': 'Mozilla/5.0'})
        html_doc = urlopen(req).read()
        soup = BeautifulSoup(html_doc,'lxml')
        ol = soup.find('ol',{'class':'reviews critic_reviews'})
        critic_elements = 0
        if ol:
            critic_elements = ol.find_all('li',{'class':'review critic_review'})
            #If statement to check if there is at least one review
        if soup.find('li',{'class':'review critic_review first_review'}):
            f_r = self.get_special_review(soup.find('li',{'class':'review critic_review first_review'}), False)
            if self.reviews:
                self.critic_reviews[f_r[0]] = {'review':f_r[1], 'score':f_r[2]}
            else:
                self.critic_reviews[f_r[0]] = {'score':f_r[1]}
        #If statement to check if there are at laest two 
        if soup.find('li',{'class':'review critic_review last_review'}):
            l_r = self.get_special_review(soup.find('li',{'class':'review critic_review last_review'}), False)
            if self.reviews:
                self.critic_reviews[l_r[0]] = {'review':l_r[1], 'score':l_r[2]}
            else:
                self.critic_reviews[l_r[0]] = {'score':l_r[1]}
        #If statement to check if there is only one review
        elif soup.find('li',{'class':'review critic_review first_review last_review'}):
            only_review = self.parse_tag(
                    soup.find('li',{'class':'review critic_review first_review last_review'}))
            if self.reviews:
                self.critic_reviews[only_review[0]] = {'review':only_review[1],
                                        'score':only_review[2]}
            else:
                self.critic_reviews[only_review[0]] = {'score':only_review[1]}
        #If statement in case there are more than 2 reviews
        if critic_elements:
            for critic_review in critic_elements:
                data = self.parse_tag(critic_review)
                if self.reviews:
                    self.critic_reviews[data[0]] = {'review':data[1], 'score':data[2]}
                else:
                    self.critic_reviews[data[0]] = {'score':data[1]}
        # if pool = 1 and there are more reviews on a different webpage:
        #         get all the user reviews for next page
        if self.pool and soup.find('a', {'class':'action','rel':'next'}, href=True):
            self.get_user_reviews(url, page+1)
        return self.critic_reviews

    #extrace li element literals
    def parse_tag(self, tag_data):
        if self.reviews:
            return (
                    tag_data.find('a',href=True).getText(),
                    tag_data.find('div',{'class':'review_body'}).getText(),
                    tag_data.find('div',{'class':'metascore_w'}).getText())                    
        return (
                tag_data.find('a',href=True).getText(),
                tag_data.find('div',{'class':'metascore_w'}).getText())

    #extract first and last review 
    def get_special_review(self, tag, user=True):
        if user:
            tag_data = self.parse_tag(tag)
            if self.reviews:
                return(tag['id'],tag_data[0],tag_data[1],
                       tag_data[2])
            return(tag['id'],tag_data[0],tag_data[1])
        else:
            tag_data = self.parse_tag(tag)
            if self.reviews:
                return(tag_data[0],tag_data[1],
                       tag_data[2])
            return(tag_data[0],tag_data[1])
    
    #Calculate averages for user and critic reviews. 
    def calculateAvgs(self):
        user_avg = sum([int(self.user_reviews[k]['score']) 
                        for k in self.user_reviews])/len(self.user_reviews)
        self.user_reviews['average'] = round(user_avg,1)
        crit_avg = sum([int(self.critic_reviews[k]['score']) 
                        for k in self.critic_reviews])/len(self.critic_reviews)
        self.critic_reviews['average'] = round(crit_avg)
    
    #calculate the total number of times x rating occurs for users
    def userTotals(self):
        self.user_reviews['totals'] = {}
        #0-4 negative(red), 5-7 mixed(yellow),8-10 positive(green) 
        for _id in self.user_reviews :
            #Skip the average and totals key, as they do not contain reviews.
            if _id == 'average' or _id == 'totals':#skip through these keys
                continue                           #as they are not reviews
            rating = int(self.user_reviews[_id]['score'])
            self.user_reviews['totals'][rating] = \
                self.user_reviews['totals'].get(rating, 0) + 1
            if rating < 5 : 
                self.user_reviews['totals']['negative'] = \
                        self.user_reviews['totals'].get('negative', 0) + 1
            elif rating < 8 :
                self.user_reviews['totals']['mixed'] = \
                        self.user_reviews['totals'].get('mixed', 0) + 1
            else :
                self.user_reviews['totals']['positive'] = \
                        self.user_reviews['totals'].get('positive', 0) + 1
            self.user_reviews['totals']['num_of_reviews'] = \
                self.user_reviews['totals'].get('num_of_reviews', 0) + 1
    
    #calculate the toatl number of times x rating occurs for critics
    def criticTotals(self):
        self.critic_reviews['totals'] = {}
        for _id in self.critic_reviews:
            if _id == 'average' or _id == 'totals':#skip through these keys as
                continue                           #they are not reviews
            rating = int(self.critic_reviews[_id]['score'])
            self.critic_reviews['totals'][rating] = \
                self.critic_reviews['totals'].get(rating, 0) + 1
            if rating < 50:
                self.critic_reviews['totals']['negative'] = \
                    self.critic_reviews['totals'].get('negative', 0) + 1
            elif rating < 75:
                self.critic_reviews['totals']['mixed'] = \
                    self.critic_reviews['totals'].get('mixed', 0) + 1
            else: 
                 self.critic_reviews['totals']['positive'] = \
                     self.critic_reviews['totals'].get('positive', 0) + 1
            self.critic_reviews['totals']['num_of_reviews'] = \
                self.critic_reviews['totals'].get('num_of_reviews', 0) + 1
                
    #standard __repr__ method
    def __repr__(self):
        return 'PyGameCritic("{0}", "{1}", critics={2},users={3}, pool={4},'\
                ' reviews={5})'.format(self.console,self.game,self.critics,
                                self.users,self.pool,self.reviews)
    
    #print method call __str__
    def __str__(self):
        return '{0} for {1} has {2} user reviews and {3} critic reviews'.
                    format(self.game.title(),self.console.title(),
                        len(self.user_reviews)-2,len(self.critic_reviews)-2)
        
if __name__ == '__main__':
    #set pool to 1 to test if script pulls all reviews.
    try:
        PyGameCritic(input('Enter the console:').strip()
                            ,input('Enter the game:').strip())
                            

    except Exception as e:
        raise Exception(
            "Ran into an error, most likely mispelled console or game title",
            'System error :',e)