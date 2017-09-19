import unittest
from unittest.mock import Mock
from datagetter import CryptoCurrencyData

class TestCryptoCurrencyData(unittest.TestCase):
    def setUp(self):
        coin_mock = [
                {
	"id":"bitcoin",
	"name": "Bitcoin", 
        "symbol": "BTC", 
        "rank": "1", 
        "price_usd": "3634.57", 
        "price_btc": "1.0", 
        "24h_volume_usd": "1281140000.0", 
        "market_cap_usd": "60232319383.0", 
        "available_supply": "16572062.0", 
        "total_supply": "16572062.0", 
        "percent_change_1h": "0.63", 
        "percent_change_24h": "1.87", 
        "percent_change_7d": "-11.85", 
        "last_updated": "1505668766", 
        "price_pln": "13012.3057855", 
        "24h_volume_pln": "4586673371.0", 
        "market_cap_pln": "215640738240"
                }]
        CryptoCurrencyData._get_coin_info = Mock(return_value=coin_mock)
        self.bitcoin = CryptoCurrencyData('bitcoin','pln')

    def test_price(self):
        self.assertEqual(self.bitcoin.price(), '13012.3057855')
        self.assertEqual(self.bitcoin.percent_change_one_hour(), '0.63')


if __name__ == '__main__':
    unittest.main()
