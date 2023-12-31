import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

VERIFIED_NUMBER = "+917751002939"
VIRTUAL_TWILIO_NUMBER = "+17086956184"

account_sid = 'AC6732f022baddf15356f59bc409a7254c'
auth_token = 'bf6162df1971782484bf6260a86b2ecd'

STOCK_API_KEY = "35M5DWGDQQIZCSGM"
news_artical_api = "57b3d3460adb4b778362cb5143d86a23"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
new_list = [value for (key, value) in data.items()]
yesterday_close_price = new_list[0]['4. close']
print(yesterday_close_price)
# TODO 2. - Get the day before yesterday's closing stock price
day_before_yesterday_close_price = new_list[1]['4. close']
print(day_before_yesterday_close_price)

# TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
diffrence = abs(float(yesterday_close_price) - float(day_before_yesterday_close_price))
up_down = None
if diffrence > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

# TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percentage_diff = round((diffrence / float(yesterday_close_price)) * 100)
print(percentage_diff)
# TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
if abs(percentage_diff) < 5:
    news_parameter = {
        "apikey": news_artical_api,
        "qInTitle": COMPANY_NAME
    }

    ## STEP 2: https://newsapi.org/
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

    # TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameter)
    articles = news_response.json()["articles"]
    # print(articles)
    # TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    three_articles = articles[:3]
    print(three_articles)

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    # to send a separate message with each article's title and description to your phone number.

    # TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension
    article_list = [
        f"{STOCK_NAME}: {up_down}{percentage_diff}%\nHeadline: {article['title']}. \nBrief: {article['description']}"
        for article in three_articles]
    print(article_list)
    client = Client(account_sid, auth_token)

    for article in article_list:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )

# TODO 9. - Send each article as a separate message via Twilio.
