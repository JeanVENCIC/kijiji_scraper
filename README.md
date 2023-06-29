# kijiji_scraper
Python toy project to automatically scrap specific Kijiji webpages and notify every new ad by discord dm.


## Requirements
For the script to work you'll have to :
- activate the dev mode on the desired discord account that will send the notifications
- get the [discord token id](https://discordhelp.net/discord-token) of the notifier account and write it in the scraper.py file as the TOKEN global variable
- get the [discord channel id](https://docs.statbot.net/docs/faq/general/how-find-id/) (can be a server channel or a dm channel) and write it in the scraper.py file as the CHANNEL_ID global variable

## Good to know
- ads already encountered will be stored in a pickle file
- the time between 2 webpage scraps (--timer) should not be set to 1 for it causes an IP timeout by kijiji

