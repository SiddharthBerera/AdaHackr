from requests import Request, Session
import json
import pprint
import time
from datetime import datetime
import csv
import websocket
from binance.client import Client
from binance_api_keys import api_key, api_secret

client = Client(api_key, api_secret)
client.API_URL = 'https://testnet.binance.vision/api'


def start():

    """
    start time
    we only want to proceed when we are at the beginning of a minute, so stuck until seconds is at beginning of minute
    i.e. when time is form hour:min:00
    """
    beginning_of_min = False
    while beginning_of_min == False:
        start_at = datetime.now()
        start_time_sec = start_at.strftime("%H:%M:%S")
        start_time_min = start_at.strftime("%H:%M")
        if start_time_sec[-2:] == '00':
            beginning_of_min = True 
 
    print("Starting at", start_time_sec)
    return start_time_sec

#def get_historical data():

def create_latest_data():

    #get btc data currently and store price data every minute
    #i is minute counter starting from min 0
    i=0
    #set up price and times array
    times = []
    prices = []

    #create data_file
    fieldnames = ["minute", "time", "price"]
    with open('data.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    #keep on getting new data every minute
    while True:

        #get price first (so most accurate although this is a matter of nano seconds probably)
        prices.append(float(client.get_symbol_ticker(symbol="BTCUSDT")['price']))
        #get time 
        now = datetime.now()
        current_time = now.strftime("%H:%M")
    
        #print price and time (testing purposes)
        print("Current Time =", current_time)
        print(prices)
        times.append(current_time)
        print(times)

        info = {
            "minute": i,
            "time": times[i],
            "price": prices[i]
            }
    
        #open file to write minute, time, price
        with open('data.csv', 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writerow(info)
    
        #increment minute counter and get data in 60 seconds (noob api version)
        i+=1
        time.sleep(60)

def main():
    start_time_sec = start()
    create_latest_data()
main()
