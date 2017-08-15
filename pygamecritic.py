from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

''' 
    Testing proved a bit buggy, after multiple tests and lots of html reviews,
    I have concluded that some of metacritics reviews get pulled from the site.
    Many of the pulled reviews are actual critic reviews, not user reviews.
    Due to this fact, many of the sites numbers are inaccurate. 
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
# Static dicts make it easier to retrieve all user/critic reviews
user_reviews = {}
critic_reviews = {}

#Main method, pool parameter used to determine whether we want all reviews or
#just one page full
def get_all_metacritic_data(console, game, critics=True, users=True, pool=1): 
    url = 'http://www.metacritic.com/game/{0}/{1}' \
        .format(console.replace(' ','-'),game.replace(' ','-'))
    results = {}
    if critics : results['critics'] = get_critic_reviews(url,pool)
    if users : results['users'] = get_user_reviews(url,pool)
    print('Number of user reviews: ',len(user_reviews))
    print('Number of critic reviews: ',len(critic_reviews))
    for j in critic_reviews.keys():
        print(j)
    return results

#get user reviews
def get_user_reviews(url, pool, page=0):
    req = Request(url + '/user-reviews?page=' + str(page) 
                    , headers={'User-Agent': 'Mozilla/5.0'})
    html_doc = urlopen(req).read()
    soup = BeautifulSoup(html_doc,'lxml')
    ol = soup.find_all('ol',{'class':'reviews user_reviews'})
    user_elements = 0
    if ol:
            user_elements = ol[0].find_all('li',{'class':'review user_review'})
    #If statements to check if there is only one review
    if soup.find('li',{'class':'review user_review first_review last_review'}):
        only_review = parse_tag(
            soup.find('li',{'class':'review user_review first_review last_review'}))
        user_reviews[only_review[0]] = {'name':only_review[1],
                    'review':only_review[2],'score':only_review[2]}
    #If statement to check if there is at least one review
    if soup.find('li',{'class':'review user_review first_review'}) :
        f_r = get_special_review(soup.find('li',{'class':'review user_review first_review'}))
        user_reviews[f_r[0]] = {'name':f_r[1], 'review':f_r[2], 'score':f_r[3]}
    #If statement to check if there is at laest two 
    if soup.find('li',{'class':'review user_review last_review'}): 
        l_r = get_special_review(soup.find('li',{'class':'review user_review last_review'}))
        user_reviews[l_r[0]] = {'name':l_r[1], 'review':l_r[2], 'score':l_r[3]}
    # necessary if statement in case there are less than 3 reviews
    if user_elements: 
        for user_review in user_elements:
            data = parse_tag(user_review)
            user_reviews[user_review['id']] = {'name':data[0],
                    'review':data[1], 'score':int(data[2])}
    # if pool = 1 and there are more reviews on a different webpage:
    #         get all the user reviews for next page    
    if pool and soup.find('a', {'class':'action','rel':'next'}, href=True):
        get_user_reviews(url, pool, page+1)
    return user_reviews

# get critic rerviews
def get_critic_reviews(url, pool, page=0):
    req = Request(url + '/critic-reviews?page=' + str(page)
                  , headers={'user-Agent': 'Mozilla/5.0'})
    html_doc = urlopen(req).read()
    soup = BeautifulSoup(html_doc,'lxml')
    ol = soup.find_all('ol',{'class':'reviews critic_reviews'})
    critic_elements = 0
    if ol:
        critic_elements = ol[0].find_all('li',{'class':'review critic_review'})
    #If statement to check if there is only one review
    if soup.find('li',{'class':'review critic_review first_review last_review'}):
        only_review = parse_tag(
            soup.find('li',{'class':'review critic_review first_review last_review'}))
        critic_reviews[only_review[0]] = {'review':only_review[1]
                                ,'score':only_review[2]}
    #If statement to check if there is at least one review
    if soup.find('li',{'class':'review critic_review first_review'}):
        f_r = get_special_review(soup.find('li',{'class':'review critic_review first_review'}), False)
        critic_reviews[f_r[0]] = {'review':f_r[1], 'score':f_r[2]}
    #If statement to check if there is at laest two 
    if soup.find('li',{'class':'review critic_review last_review'}):
        l_r = get_special_review(soup.find('li',{'class':'review critic_review last_review'}), False)
        critic_reviews[l_r[0]] = {'review':l_r[1], 'score':l_r[2]}
    #If statement in case there are more than 2 reviews
    if critic_elements:
        for critic_review in critic_elements:
            data = parse_tag(critic_review)
            critic_reviews[data[0]] = {'review':data[1], 'score':data[2]}
    # if pool = 1 and there are more reviews on a different webpage:
    #         get all the user reviews for next page
    if pool and soup.find('a', {'class':'action','rel':'next'}, href=True):
        get_user_reviews(url, pool, page+1)
    return critic_reviews

#extrace li element literals
def parse_tag(tag_data):
    return (
            tag_data.find('a',href=True).getText(),
            tag_data.find('div',{'class':'review_body'}).getText(),
            tag_data.find('div',{'class':'metascore_w'}).getText())

#extract first and last review 
def get_special_review(tag, user=True):
    if user:
        tag_data = parse_tag(tag)
        return(tag['id'],tag_data[0],tag_data[1],
               int(tag_data[2]))
    else:
        tag_data = parse_tag(tag)
        return(tag_data[0],tag_data[1],
               int(tag_data[2]))

if __name__ == '__main__':
    #set pool to 1 to test if script pulls all reviews.
    try:
        get_all_metacritic_data(input('Enter the console:').strip()
                            ,input('Enter the game:').strip().lower(),pool=0)
    except Exception:
        raise Exception(
            "Ran into an error, most likely mispelled console or game title")