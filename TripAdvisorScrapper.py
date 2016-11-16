#Eric Park
#Python 2.7
#TripAdvisor Scrapper
import urllib
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool
import csv

#Potential Imports
import re
from threading import Thread
from Queue import Queue
import time

#List of TripAdvisor urls to scrape
#This is Scrapping Select Oyster Bar Pages
url=['https://www.tripadvisor.com/Restaurant_Review-g60745-d7906359-Reviews-Select_Oyster_Bar-Boston_Massachusetts.html','https://www.tripadvisor.com/Restaurant_Review-g60745-d7906359-Reviews-or10-Select_Oyster_Bar-Boston_Massachusetts.html#REVIEWS','https://www.tripadvisor.com/Restaurant_Review-g60745-d7906359-Reviews-or20-Select_Oyster_Bar-Boston_Massachusetts.html#REVIEWS','https://www.tripadvisor.com/Restaurant_Review-g60745-d7906359-Reviews-or30-Select_Oyster_Bar-Boston_Massachusetts.html#REVIEWS']

#function that will do actual scraping job
def scrape(ur):
    ans = []
    html = urllib.urlopen(ur).read()
    soup = BeautifulSoup(html)


    for users in soup.findAll('div', {'class': 'deckB review_collection '}):
        ans = []

        loc = ""
        rating = ""
        review = ""
        usefulCount = ""
        #Get Location
        count = 0
        for user in users.findAll('div', {'class': 'location'}):
            loc = user.get_text()
            loc = loc.replace('\n','')
            ans.append([loc.encode('utf8')])
            count += 1

        #Get Rating
        count = 0
        for user in users.findAll('span', {'class': 'rate sprite-rating_s rating_s'}):
            for image in user.findAll("img"):
                alt = image.get('alt', '')
                if alt == "1 of 5 bubbles":
                    rating = 1
                if alt == "2 of 5 bubbles":
                    rating = 2
                if alt == "3 of 5 bubbles":
                    rating = 3
                if alt == "4 of 5 bubbles":
                    rating = 4
                if alt == "5 of 5 bubbles":
                    rating = 5
                ans[count].append(rating)
                count += 1

        # Get Review
        count = 0
        for comment in users.findAll('p', {'class': 'partial_entry'}):
            review = (comment.get_text()).replace('<br>',' ')
            review = review.replace('\n','')
            ans[count].append(review.encode('utf8'))
            count += 1

        #Remove all but useful
        #In this case, we remove anyone who does not have a location
        count = 0
        for user in users.findAll('div', {'class': 'location'}):
            loc = user.get_text()
            loc = loc.replace('\n','')
            if loc == '':
                ans = ans[:count] + ans[count + 1:]
            else:
                count += 1
    return ans




threadlist = []
ans = []
i=0

#making threads
pool = ThreadPool(processes=4)


while i<len(url):
    async_result = pool.apply_async(scrape, [url[i].encode('utf8')])
    #t = Thread(target=scrape,args=(url[i],))
    #t.start()
    #threadlist.append(t)
    #time.sleep(1)
    return_val = async_result.get()
    for j in range(len(return_val)):
        ans.append(return_val[j])
    i=i+1

for b in threadlist:
    b.join()

with open("ScrapeOutputs/TripAdvisorOutput.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(ans)


