import argparse
import time
from os import path
import pickle
import requests
from bs4 import BeautifulSoup

URL_KIJIJI = "https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/3+1+2__3+1+2+et+coin+detente__4+1+2__4+1+2+et+coin+detente__5+1+2/c37l1700281a27949001?radius=3.0&price=__1020&address=Av+du+Parc%2C+Montr%C3%A9al%2C+QC+H2W%2C+Canada&ll=45.513343,-73.581700"
USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0"
TOKEN = "MTY0MDg1MDEzNDg1MTkxMTY4.Yh44BA.uSKH4U_oCAAh8PTm6lFNTektYp8"
CHANNEL_ID = "641315485132259328"


def main():
    parser = argparse.ArgumentParser(description='Scrap Kijiji scpecific url for new add and notify discord chan.')

    parser.add_argument('-u', '--url', action='store', dest='url', type=str, default=URL_KIJIJI, help='Kijiji url to scrap.')
    parser.add_argument('-t', '--timer', action='store', dest='timer', type=int, default=5, help='Timer between each scrap in minutes.')
    parser.add_argument('-p', '--path_pickle', action='store', dest='path_pickle', type=str, default="ads_dict.pickle", help='path to pickle with stored ads info.')
    parser.add_argument('-id', '--channel_id', action='store', dest='channel_id', type=str, default=CHANNEL_ID, help='Discord channel id to notify of newly found ad.')
    parser.add_argument('--token', action='store', dest='token', type=str, default=TOKEN, help='Discord token for authorization.')
    parser.add_argument('--user_agent', action='store', dest='user_agent', type=str, default=USER_AGENT, help='user-agent to use in requests.post call.')
    parser.add_argument("--silent", action = "store_true", dest='silent', help = "Flag to run without notifying.")

    args = parser.parse_args()

    starttime = time.time()
    print("staring at : " + str(time.ctime()))

    while True :
        print("Scraping : " + str(time.ctime()))

        ads_dict = load_ads_dict(args.path_pickle)

        soup = get_soup(args.url, args.user_agent)

        new_ads_dict = parse_soup(soup, ads_dict, not args.silent)

        if len(new_ads_dict) == 0:
            print("No new ads :(")
        else:
            print("{} new ads :)".format(str(len(new_ads_dict))))

            for id in new_ads_dict:
                new_ad = new_ads_dict[id]
                
                print("\t"+str(new_ad))

                if not (args.silent):
                    notify(args.token, args.channel_id, new_ad["url"])

                ads_dict[id] = new_ad


        save_ads_dict(ads_dict, args.path_pickle)

        time.sleep(args.timer*60)


def notify(token = TOKEN, channel_id = CHANNEL_ID, message = "hello there"):
    url = "https://discord.com/api/v9/channels/{}/messages".format(channel_id)
    data = {"content": message}
    header = {"authorization": token, "content-type": "application/json"}

    r = requests.post(url, json=data, headers=header)

    return(r.status_code)

def load_ads_dict(path_to_pickle = "ads_dict.pickle"):
    if(path.exists(path_to_pickle)):
        with open(path_to_pickle, 'rb') as handle:
            ads_dict = pickle.load(handle)
            return(ads_dict)
    else:
        return(dict())

def save_ads_dict(ads_dict, path_to_pickle = "ads_dict.pickle"):
    with open(path_to_pickle, 'wb') as handle:
        pickle.dump(ads_dict, handle)

def get_soup(url = URL_KIJIJI, user_agent = USER_AGENT):

    headers = {
        "User-Agent": USER_AGENT
    }

    page = requests.get(url, headers=headers)
    if not (page.status_code == 200):
        pass

    page.close()

    soup = BeautifulSoup(page.content, 'html.parser')

    return(soup)


def parse_soup(soup, ads_dict, notify_bool=False) :
    new_ads_dict = {}
    
    ads = soup.find_all("div", {"class", "search-item regular-ad"})

    for ad in ads:
        id_kijiji = int(ad.attrs["data-listing-id"])
        price = int(ad.find("div", {"class":"price"}).text.strip().replace("\xa0", "").split(",")[0])
        title = ad.find("div", {"class", "title"}).text.strip()
        url = "https://www.kijiji.ca" + ad.attrs["data-vip-url"]

        if(id_kijiji not in ads_dict):
            # New add !
            new_ads_dict[id_kijiji] = {"title":title, "price":price, "url":url}

    return(new_ads_dict)

if __name__ == "__main__":
    main()
