import json
import pprint
import time
from time import sleep
from datetime import datetime
import csv
from binance.client import Client
from binance import ThreadedWebsocketManager
from binance_api_keys import api_key, api_secret
import websocket
import numpy
from binance.enums import *

socket = "wss://stream.binance.com:9443/ws/btcbusd@kline_1m"

trade = 'BTCBUSD'

closes = []

client = Client(api_key, api_secret)

#initilise global variablz
i=0
#in unix time stamp in milliseconds
times = []
open_prices = []
high_prices = []
low_prices = []
close_prices = []

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
    # in hours, min and sec
    return start_time_sec
    
def create_latest_data():
    #create data_file
    fieldnames = ["time", "open", "high", "low", "close"]
    with open('data.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

#def get_historical_data(time_period):

def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def on_message(ws, message):
    #make these global so we can append to them
    global times, open_prices, high_prices, low_prices, close_prices, i

    print("recieved message")
    

    json_message = json.loads(message)
    print(json_message)
    candle = json_message['k']
    is_candle_closed = candle['x']
    #when candle for minute is closed extract open, close, high and low prices for candle
    if is_candle_closed:
        #start time for candlestick as unix timestamp in milliseconds
        times.append(candle['t'])
        #o,h,l,c prices
        open_prices.append(candle['o'])
        print(type(open_prices[i]))
        high_prices.append(candle['h'])
        low_prices.append(candle['l'])
        close_prices.append(candle['c'])

        #create latest row in data frame
        info = {
            "time": times[i], 
            "open": open_prices[i], 
            "high": high_prices[i], 
            "low": low_prices[i],
            "close": close_prices[i], 
            }

        fieldnames = ["time", "open", "high", "low", "close"]
        #open file to write timestamp, open, close, high and low prices
        with open('data.csv', 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writerow(info)
        i+=1

def main():        
    start_time_sec = start() 
    #get_historical_data
    create_latest_data()       
    ws = websocket.WebSocketApp(socket, on_open=on_open, on_close=on_close, on_message=on_message)
    ws.run_forever()

main()




