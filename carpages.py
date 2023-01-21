
                                        #carpages.ca crawler
                ##################################################################
                #                                                                #
                #           coded with pain and love by Ayoub Elakhdar           #
                #                                                                #
                ##################################################################


## links
## car's name
## price
## car's type

#importing the packages
from pandas import DataFrame as dt
from bs4 import BeautifulSoup
import requests

#the page graber function
def graber(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    return soup
    
#setting up the crawler and getting the initial page
pageCount = 0 # used to count the pages in the website and stops at 59
url = 'https://www.carpages.ca/used-cars/search/?fueltype_id%5B0%5D=3&fueltype_id%5B1%5D=7'
soup = graber(url)    
sheet = dt({'Links':[''], 'Names':[''], 'Prices':[''], 'Car Type':['']})

#initiating the crawler
while pageCount < 59: 
    #grabing all the listings
    posts = soup.find_all('div', class_ = 'media soft push-none rule')
    
    #grabing each lising info each
    for post in posts:
        link = 'http://carpages.ca'+post.find('a', class_ = 'media__img media__img--thumb').get('href')
        carName = post.find('h4', class_ = 'hN').text.strip()
        price = post.find('strong', class_ = 'delta').text.strip()
        carType = post.find('p', class_ = 'hN').text.strip()
        sheet.loc[len(sheet)] = [link,carName,price,carType]
    
    #updating the url with next page link
    if pageCount < 57:
        #grab the next page url only if still there is a next page
        url = 'http://carpages.ca'+soup.find('a', {'title':'Next Page'}).get('href')
        soup = graber(url)
    else:
        #or just pass getting a link that it's not excist
        pass
    
    #updating the loop counter
    pageCount += 1

#extracting the dataFrame as a csv for later processing
sheet.to_csv('C:/Users/user/Desktop/cars.csv')
print('scraping process ended successfully')