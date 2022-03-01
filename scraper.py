import requests
import pickle
from bs4 import BeautifulSoup

URL = "https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/3+1+2__3+1+2+et+coin+detente__4+1+2-appartement/c37l1700281a27949001a29276001?price=__1000"
USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0"

def notify(ad_info):
    pass

def load_ads_dict(path = "ads_dict.pickle"):
    return(pickle.load(path))

def save_ads_dict(ads_dict, path = "ads_dict.pickle"):
    with open('filename.pickle', 'wb') as handle:
        pickle.dump(ads_dict, handle)

def get_soup(url = URL, user_agent = USER_AGENT):

    headers = {
        "User-Agent": USER_AGENT
    }

    page = requests.get(url, headers=headers)
    if not (page.status_code == 200):
        pass

    page.close()

    soup = BeautifulSoup(page.content, 'html.parser')

    return(soup)


def parse_soup(soup, ads_dict) :
    ads = soup.find_all("div", {"class", "search-item regular-ad"})

    for ad in ads:
        id_kijiji = int(ad.attrs["data-listing-id"])
        price = int(ad.find("div", {"class":"price"}).string.strip().removesuffix("\xa0$"))
        title = ad.find("div", {"class", "title"}).text.strip()
        link = "www.kiji.ca" + ad.attrs["data-vip-url"]

        if(id_kijiji not in ads_dict):
            # New add !
            ads_dict[id_kijiji] = {"title":title, "price":price, "link":link}
            
            notify(ads_dict[id_kijiji])

    return(ads_dict)

def main():
    pass