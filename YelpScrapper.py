#Eric Park
#Python 2.7
#Yelp Scrapper

import urllib
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool
import threading
import csv

#Potential Imports
import re
from threading import Thread
from Queue import Queue

#List of yelp urls to scrape
#This is Scrapping Select Oyster Bar Pages
url=['https://www.yelp.com/biz/select-oyster-bar-boston?sort_by=date_desc','https://www.yelp.com/biz/select-oyster-bar-boston?start=20&sort_by=date_desc','https://www.yelp.com/biz/select-oyster-bar-boston?start=40&sort_by=date_desc']

#function that will do actual scraping job
def scrape(ur):

    html = urllib.urlopen(ur).read()
    soup = BeautifulSoup(html)


    for users in soup.findAll('ul', {'class': 'ylist ylist-bordered reviews'}):
        ans = []

        loc = ""
        rating = ""
        review = ""
        usefulCount = ""

        #Get Location
        count = 0
        for user in users.findAll('ul', {'class': 'user-passport-info'}):
            loc = user.find('b').get_text()
            ans.append([loc.encode('utf8')])
            count += 1

        #Get Rating
        count = 0
        for user in users.findAll('div', {'class': 'biz-rating biz-rating-very-large clearfix'}):
            for image in user.findAll("img"):
                alt = image.get('alt', '')
                if alt == "1.0 star rating":
                    rating = 1
                if alt == "2.0 star rating":
                    rating = 2
                if alt == "3.0 star rating":
                    rating = 3
                if alt == "4.0 star rating":
                    rating = 4
                if alt == "5.0 star rating":
                    rating = 5
                ans[count].append(rating)
                count += 1

        # Get Review
        count = 0
        for comment in users.findAll('p', {'lang': 'en'}):
            review = (comment.get_text()).replace('<br>',' ')
            ans[count].append(review.encode('utf8'))
            count += 1

        #Remove all but useful
        #In this case, we remove any reviews without a "Useful"
        count = 0
        for user in users.findAll('a', {'class': 'ybtn ybtn--small useful js-analytics-click'}):
            usefulCount = user.find('span', {'class': 'count'}).get_text()
            if usefulCount == "":
                ans = ans[:count] + ans[count + 1:]
            else:
                count += 1

    return ans

i=0
ans = []
csv_writer_lock = threading.Lock()
threadlist = []


#making threads
pool = ThreadPool(processes=4)


while i<len(url):
    async_result = pool.apply_async(scrape, [url[i].encode('utf8')])
    #t = Thread(target=scrape,args=(url[i],))
    #t.start()
    #threadlist.append(t)
    return_val = async_result.get()
    for j in range(len(return_val)):
        ans.append(return_val[j])
    i=i+1

for b in threadlist:
    b.join()

with open("ScrapeOutputs/YelpOutput.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(ans)


