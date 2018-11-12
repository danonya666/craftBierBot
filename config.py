import re

from beer import Beer

welcoming_string = "Добро пожаловать! Меня зовут Craft Bier Bot. Я служу во имя Craft Bier Cafe! Чем могу быть полезен?"

query_messages = {"BbC": "beer by countries",
                  "BbS": "beer by sorts",
                  "BfL": "beer full list",
                  "bBbC": "bottled beer by countries",
                  "bBbS": "bottled beer by sorts",
                  "bBfL": "bottled beer full list"}

test_beer_list = [Beer("Meizels Weisse", "Germany", "some brewery", 10, 5.5, "https://untappd.com/b/brauerei-gebr-maisel-maisel-s-weisse-original/35642", type="Weize beer", bottled=False),
                  Beer("French Beer", "France", "some brewery", 10, 5.5, "https://untappd.com/b/ratio-beerworks-dear-you/955352", "French Type", False),
                  Beer("Second German beer", "Germany", "some brewery", 10, 5.5, "https://untappd.com/b/warsteiner-warsteiner-premium-verum-german-pilsener/10703", type="Warsteiner", bottled=False)]

bottled_beer_list = [Beer("bottle1", "Russia", "brewery1", 7, 15, "https://vk.com", "IPA", True)]
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
proxy_list = ['http://69.70.219.202:56946/', 'http://87.120.152.14:23500', 'http://194.135.108.230:59826/', 'http://190.192.73.238:50892']


def flag(country):
    return flag_dictionary[country]


flag_dictionary = {"Germany": "🇩🇪",
                   "Russia": "🇷🇺",
                   "France": "🇫🇷",
                   "Belgium": "🇧🇪"}

first_beer = test_beer_list[0]