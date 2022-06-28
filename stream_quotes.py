from statistics import mode
from alpaca_trade_api.stream import Stream
from datetime import datetime,timedelta
from anyio import current_time
import pandas as pd
import logging
import dummy
import os
import time

API_KEY = "PK12GXXW6Q5S989MB9SC"
SECRET_KEY = "z6HrTmiOsWbB2q4EpU63lIXf4rP773ix26HqPIy4"

def csv_handling(file_name: str, columns_list: list):
    if os.path.exists(file_name):
        try:
            trade_temp_df = pd.read_csv(file_name)
        except:
            print("The file doesn't exist, creating it")
            trade_temp_df = pd.DataFrame(columns=columns_list)
            trade_temp_df.to_csv(file_name)
        if trade_temp_df.empty:
            trade_temp_df = pd.DataFrame(columns=columns_list)
            trade_temp_df.to_csv(file_name)
        else:
            pass
    else:
        trade_temp_df = pd.DataFrame(columns=columns_list)
        trade_temp_df.to_csv(file_name)

async def trade_trades(trades):
    temp_df = pd.DataFrame(
        columns=["time", "price", "size", "ID", "tic","exchange"]
    )
    
    present_time = datetime.utcfromtimestamp(trades.timestamp/10**9).strftime("%Y-%m-%d %H:%M:%S")
    temp_df["time"] = [present_time]
    temp_df['price'] = [trades.price]
    temp_df['size'] = [trades.size]
    temp_df['ID'] = [trades.id]
    temp_df['tic'] = [trades.symbol]
    temp_df['exchange'] = [trades.exchange]

    temp_df.to_csv("trades.csv", mode="a", header=False)


async def trade_quotes(quotes):
    temp_df = pd.DataFrame(
        columns=["time", "Ask Price", "Bid Price", "Ask Size", "Bid Size", "tic", "exchange"]
    )
    
    present_time = datetime.utcfromtimestamp(quotes.timestamp/10**9).strftime("%Y-%m-%d %H:%M:%S")
    temp_df["time"] = [present_time]
    temp_df['Ask Price'] = [quotes.ask_price]
    temp_df['Ask Size'] = [quotes.ask_size]
    temp_df['Bid Price'] = [quotes.bid_price]
    temp_df['Bid Size'] = [quotes.bid_size]
    temp_df['tic'] = [quotes.symbol]
    temp_df['exchange'] = [quotes.ask_exchange]

    temp_df.to_csv("trades.csv", mode="a", header=False)

def run_connection(stream):
    try:
        stream.run()
    except KeyboardInterrupt:
        print("Interrupted execution by the user")
        loop.run_until_complete(stream.stop_ws())
        exit(0)
    except Exception as e:
        print(f'Exception from websocket connection: {e}')
    finally:
        print('Trying to re-establish connection')
        time.sleep(3)
        run_connection(stream)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    dummy_path = dummy.__file__ 
    stream = Stream(
        API_KEY, SECRET_KEY, base_url="https://paper-api.alpaca.markets", raw_data=False,
        data_feed='iex',
        crypto_exchanges = ['CBSE']
    )
    stocksCount = 0
    stockUniverse = ['ETHUSD']
    csv_handling(
        "quotes.csv",
        columns_list=["time", "Ask Price", "Bid Price", "Ask Size", "Bid Size", "tic", "exchange"],
    )
    csv_handling(
        "trades.csv",
        columns_list=["time", "price", "size", "ID", "tic","exchange"],
    )
   
    stream.subscribe_quotes(trade_quotes,'AAPL')
    stream.subscribe_trades(trade_trades,'AAPL')
    run_connection(stream)
    print("Complete")