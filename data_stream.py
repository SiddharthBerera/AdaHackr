from requests import Request, Session
import json
import pprint
import time
from datetime import datetime

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

parameters = {
    "symbol":"BTC",
    "convert":"USD"
}

headers = {
    "Accepts":"application/jason",
    "X-CMC_PRO_API_KEY":"26024df9-3a05-45d9-93be-d2da0557e81f"
}

#creates a new session and uses headers information to session
session = Session()
session.headers.update(headers)

response = session.get(url, params=parameters)
#get btc data currently and store price data every minute
i=0
times = []
prices = []
#start time
start_at = datetime.now()
start_time = start_at.strftime("%H:%M:%S")
print("Start Time =", start_time)
while True:
    #get time asap (nano second delays)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    #get price next (time isn't as of the essence here since cmc noob api only updates price every min)
    prices.append(json.loads(response.text)['data']['BTC']['quote']['USD']['price'])
    
    #print price (testing purposes)
    print("Current Time =", current_time)
    print(prices)
    times.append(i)
    i+=1
    time.sleep(60)

