print("Lets do it")

import json
import websocket
import pandas as pd
from binance.client import Client
client = Client()

dict_ = client.get_exchange_info()

sym = [i['symbol'] for i in dict_['symbols'] if i['symbol'].endswith('USDT')]

print(len(sym))

sym = [i.lower() + '@kline_1m' for i in sym]

relevant = '/'.join(sym)

def manipulate(data):
    value_d = data['data']['k']
    price, sym = value_d['c'], value_d['s']
    evt_time = pd.to_datetime([data['data']['E']], unit='ms')
    df = pd.DataFrame([[price,sym]], index = evt_time)
    return df    

def on_message(ws, message):
    json_message = json.loads(message)
    df_ = manipulate(json_message)
    df_.to_csv('coinprices.csv', mode='a', header = False)
    # print(df_)
    
socket = "wss://stream.binance.com:9443/stream?streams="+relevant

ws = websocket.WebSocketApp(socket, on_message = on_message)
ws.run_forever()