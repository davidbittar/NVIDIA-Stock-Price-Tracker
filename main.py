#Setting up API's to track Nvidia's daily stock performance and get updates via text
import requests
from twilio.rest import Client

STOCK_NAME = "NVDA"
COMPANY_NAME = "NVIDIA Corporation"
TWILIO_SID = "AC0fa50fd44fc8e9de7ae328c8bf99f99c"
TWILIO_AUTH = "eded1b8117091a26a4498f49acc73da1"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API = "8b182a0ad0394c6cbca0ac71628180e7"
STOCK_API_KEY = "F9U0ICLLPYYLA1AT"
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
stocks_data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in stocks_data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data['4. close']
# print(yesterday_closing_price)


day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data['4. close']
# print(day_before_yesterday_closing_price)


difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
up_down = None
if difference > 2:
    up_down = "📈"
else:
    up_down = "📉"

percentage_diff = round((difference/float(yesterday_closing_price)) * 100)

if percentage_diff > 5:
    print("Get News")


if abs(percentage_diff) > 1:
    news_parameters = {
        "apiKey": NEWS_API,
        "qInTitle": COMPANY_NAME
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    articles = news_response.json()["articles"]
    # print(articles)

    three_articles = articles[:3]
    # print(three_articles)

    #Print json articles and see the layout and use list comprehension to create a new list

    formatted_articles = [(f"{STOCK_NAME}: {up_down}{percentage_diff}%Headline: {article['title']}. "
                           f"\nBrief: {article['description']}") for article in three_articles]


    client = Client(TWILIO_SID, TWILIO_AUTH)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_='+18558865319',
            to='+17738291888'
        )
        print(message.status)

