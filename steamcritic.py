from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

'''url = 'http://www.metacritic.com/game/playstation-4/the-witcher-3-wild-hunt/user-reviews'
req = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
html_doc = urlopen(req).read()
soup = BeautifulSoup(html_doc,'lxml')
user_elements = soup.find_all('li',{'class':'review user_review'})
user_reviews = {}
for user_review in user_elements:
    user_name = user_review.find('a',href=True).getText()
    review = user_review.find('span').getText()
    score = user_review.find('div',{'class':'metascore_w'}).getText()
    user_reviews[user_review['id']] = {'name':user_name,
                'review':review,'score':int(score)}
for k,v in user_reviews.items():
    print(k,':', v, end='\n\n\n')
   ''' 
    
url = 'http://www.metacritic.com/game/playstation-4/the-witcher-3-wild-hunt/critic-reviews'
req = Request(url,headers={'user-Agent': 'Mozilla/5.0'})
html_doc = urlopen(req).read()
soup = BeautifulSoup(html_doc,'lxml')
critic_elements = soup.find_all('li',{'class':'review critic_review'})
critic_reviews = {}
index = 0
for critic_review in critic_elements:
    critic_name = critic_review.find('a',href=True).getText()
    review = critic_review.find('div',{'class':'review_body'}).getText()
    score = critic_review.find('div',{'class':'metascore_w'}).getText()
    critic_reviews[index] = {'name':critic_name,
                  'review':review,'score':int(score)}
    index += 1

'''Both test cases are good, use ?page parameter to ask for more reviews'''