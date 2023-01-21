# carpages.ca crawler
## links
## car's name
## price
## car's type

#importing the packages
from pandas import DataFrame as dt
from bs4 import BeautifulSoup
import requests

#setting up the crawler and getting the initial page

pageCount  = 1 # used to count the pages in the website and stops at 7
url = 'https://www.carpages.ca/used-cars/search/?fueltype_id%5B0%5D=3&fueltype_id%5B1%5D=7'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')
sheet = dt({'Links':[''], 'Names':[''], 'Prices':[''], 'Car Type':['']})

#initiating the crawler
while True: 
    #grabing all the listings
    posts = soup.find_all('div', class_ = 'media soft push-none rule')
    
    #grabing each lising info each
    for post in posts:
        link = 'http://carpages.ca'+post.find('a', class_ = 'media__img media__img--thumb').get('href')
        carName = post.find('h4', class_ = 'hN').text.strip()
        price = post.find('strong', class_ = 'delta').text.strip()
        carType = post.find('p', class_ = 'hN').text.strip()
        #sheet = sheet.append({'Links':link, 'Names':carName, 'Prices':price, 'Car Type':carType}, ignore_index=True)
        sheet.loc[len(sheet)] = [link,carName,price,carType]
    
    # updating the url with next page link
    url = 'http://carpages.ca'+soup.find('a', {'title':'Next Page'}).get('href')
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    
    # this set manually and will stop once it scrapes the last page
    if pageCount > 7:
        print('scraping process ended succuffully')
        break
    else:
        pageCount += 1

# extracting the dataFrame as a csv to later processes
sheet.to_csv('C:/Users/user/Desktop/cars.csv')
