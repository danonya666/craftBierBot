from beer import Beer

api_token = "698143956:AAHIPP3ZQEQgffcC1rVf3_uQWiynOFFdqdY"
url = "https://api.telegram.org/bot698143956:AAHIPP3ZQEQgffcC1rVf3_uQWiynOFFdqdY/"
welcoming_string = "Добро пожаловать! Меня зовут Craft Bier Bot. Я служу во имя Craft Bier Cafe! Чем могу быть полезен?"

query_messages = {"BbC": "beer by countries",
                  "BbS": "beer by sorts",
                  "BfL": "beer full list"}

test_beer_list = [Beer("Meizels Weisse", "Germany", "some brewery", 10, 5.5)]
