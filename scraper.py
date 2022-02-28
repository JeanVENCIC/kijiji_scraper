import requests
from bs4 import BeautifulSoup

url = "https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/3+1+2__3+1+2+et+coin+detente__4+1+2-appartement/c37l1700281a27949001a29276001?price=__1000"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0"
}

page = requests.get(url, headers=headers)
# check code == 200
page.close()

soup = BeautifulSoup(page.content, 'html.parser')


ads = soup.find_all("div", {"class", "search-item regular-ad"})

for ad in ads:
    price = ad.find("div", {"class":"price"}).string

