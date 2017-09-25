import json
from urllib import request
import time
import datetime
import sqlite3

class CryptoCurrencyData(object):
    '''
    Class which operates on coinmarketcap api and each method returns different data about
    the cryptocurrency
    '''
    def __init__(self, coin, currency):
        self.coin = coin
        self.currency = currency
        self.json_data = self._get_coin_info()

    def _get_coin_info(self):
        with request.urlopen("https://api.coinmarketcap.com/v1/ticker/{}/?convert={}".format(self.coin, self.currency)) as url:
            return json.loads(url.read().decode())

    def coin_name(self):
        return self.coin

    def price(self):
        return self.json_data[0]["price_{}".format(self.currency)]

    def percent_change_one_hour(self):
        return self.json_data[0]["percent_change_1h"]

    def percent_change_one_day(self):
        return self.json_data[0]["percent_change_24h"]

    def percent_change_one_week(self):
        return self.json_data[0]["percent_change_7d"]
'''
Dumping data to sqlite db or single file. Every run of loop should contain datestamp and json data
'''
def main():
    bitcoin = CryptoCurrencyData('bitcoin', 'pln')
    dogecoin = CryptoCurrencyData('dogecoin', 'pln')
    currency_db = sqlite3.connect('currency.db')
    cursor = currency_db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS COINMARKET
            (COIN_NAME STR,
            COIN_PRICE REAL,
            DAY_CHANGE REAL,
            DATE UNIX);''')
    doge_name = dogecoin.coin_name()
    bit_name = bitcoin.coin_name()
    while True:
        unix = time.time()
        date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
        bit_price = float(bitcoin.price())
        doge_price = float(dogecoin.price())
        doge_name = dogecoin.coin_name()
        doge_one_hour = dogecoin.percent_change_one_hour()
        doge_one_day = float(dogecoin.percent_change_one_day())
        doge_one_week = dogecoin.percent_change_one_week()
        bitcoin_one_day = float(bitcoin.percent_change_one_day())
        cursor.execute("INSERT INTO COINMARKET (COIN_NAME ,COIN_PRICE, DAY_CHANGE, DATE)\
                VALUES (?, ?, ?, ?)",(doge_name, doge_price, doge_one_day, date))
        cursor.execute("INSERT INTO COINMARKET (COIN_NAME, COIN_PRICE, DAY_CHANGE, DATE)\
                VALUES (?, ?, ?, ?)",(bit_name, bit_price, bitcoin_one_day, date))
        currency_db.commit()

        time.sleep(300)
if __name__ == '__main__':
    main()
