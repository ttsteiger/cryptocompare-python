
# cryptocompy

Simple wrapper for the public CryptoCompare API.

Cryptocompare API:
https://www.cryptocompare.com/api

## Table of Contents

* [ToDo](#ToDo)
* [Installation](#Installation)
* [Code of Conduct](#code-of-conduct)
* [Contributing](#Contributing)
* [Documentation](#Documentation)
    * [coin.py](#coinpy)
        * [get_coin_list](#get_coin_list)
        * [get_coin_snapshot](#get_coin_snapshot)
    * [price.py](#pricepy)
        * [get_current_price](#get_current_price)
        * [get_current_trading_info](#get_current_trading_info)
        * [get_day_average_price](#get_day_average_price)
    * [mining.py](#miningpy)
        * [get_mining_contracts](#get_mining_contracts)
        * [get_mining_equipment](#get_mining_equipment)
    * [top.py](#toppy)
        * [get_top_exchanges](#get_top_exchanges)
        * [get_top_coins](#get_top_coins)
        * [get_top_pairs](#get_top_pairs)

## ToDo:

- add all get functions
- complete docstrings
- create readme with examples
- error handling for http requests
- throw warnings for conversions
- add toTs parameter to price functions
- improve date handling in historical price functions
- add folder with some more complex example code (for eg. compare average mining equipment prices graphically)

- both mining contracts and equipment calls return same message -> tell CC Support?


## Installation

pip install cryptocompy

## Code of Conduct

Dont abuse wrapper to spam the Cryptocompare API. A request every 10 seconds should be more than enough.

## Contributing

If you would like to help me with my work or have any suggestions for improvements please follow the "fork-and-pull" Git workflow.

1. Fork the repo on GitHub
2. Clone the project to your own machine
3. Commit changes to your own branch
4. Push your work back up to your fork
5. Submit a Pull request so that we can review your changes

NOTE: Be sure to merge the latest from "upstream" before making a pull request!


## Documentation

### coin.py

To access these functions, you can import them in the following way:


```python
from cryptocompy import coin
```

---

#### get_coin_list

```python
get_coin_list(coins='all')
```

Get general information about all the coins available on cryptocompare.com.

*Arguments:*

`coins`: Default value of `'all'` returns information about all the coins available on the site. Otherwise a single string or list of coin symbols can be used.

*Returns:*

The function returns a dictionairy containing individual dictionairies for the coins specified by the input. The key of the top dictionary corresponds to the coin symbol. The dictionary returned has the following structure:

```
{coin_symbol1: {'Algorithm' : ...,
                'CoinName': ...,
                'FullName': ...,
                'FullyPremined': ...,
                'Id': ...,
                'ImageUrl': ...,
                'Name': ...,
                'PreMinedValue': ...,
                'ProofType': ...,
                'SortOrder': ...,
                'TotalCoinsFreeFloat': ...,
                'TotalCoinSupply': ...,
			    'Url': ...},
 coin_symbol2: {...},
 ...}
```

*Example 1:*

Get general coin information for Bitcoin and Ethereum.


```python
coin.get_coin_list(coins=["BTC", "ETH"])
```




    {'BTC': {'Algorithm': 'SHA256',
      'CoinName': 'Bitcoin',
      'FullName': 'Bitcoin (BTC)',
      'FullyPremined': '0',
      'Id': '1182',
      'ImageUrl': '/media/19633/btc.png',
      'Name': 'BTC',
      'PreMinedValue': 'N/A',
      'ProofType': 'PoW',
      'SortOrder': '1',
      'TotalCoinSupply': '21000000',
      'TotalCoinsFreeFloat': 'N/A',
      'Url': '/coins/btc/overview'},
     'ETH': {'Algorithm': 'Ethash',
      'CoinName': 'Ethereum ',
      'FullName': 'Ethereum  (ETH)',
      'FullyPremined': '0',
      'Id': '7605',
      'ImageUrl': '/media/20646/eth.png',
      'Name': 'ETH',
      'PreMinedValue': 'N/A',
      'ProofType': 'PoW',
      'SortOrder': '2',
      'TotalCoinSupply': '0',
      'TotalCoinsFreeFloat': 'N/A',
      'Url': '/coins/eth/overview'}}



*Example 2:*

Return information for all the coins available on Cryptocompare and print out ten of their symbols.


```python
coin_data = coin.get_coin_list()
symbols = list(coin_data.keys())[:10]
symbols
```




    ['BOSS', 'EOS', 'CHC', 'GAY', 'APT', 'DEEP', 'SCOT', 'HUGE', 'NXS', 'GCR']



---

#### get_coin_snapshot

```python
get_coin_snapshot(fsym, tsym)
```

Get blockchain information, aggregated data as well as data for the individual exchanges available for the specified currency pair.

*Arguments:*

* `fsym`: FROM symbol.
* `tsym`: TO symbol. Blockchain information will only be returned if this parameter is a fiat currency.

*Returns:*

The function returns a dictionairy containing blockain as well as trading information from the different exchanges were the specified currency pair is available.

```
{'AggregatedData': dict,
 'Algorithm': ...,
 'BlockNumber': ...,
 'BlockReward': ...,
 'Exchanges': [dict1, dict2, ...],
 'NetHashesPerSecond': ...,
 'ProofType': ...,
 'TotalCoinsMined': ...}
 
dict = {'FLAGS': ...,
        'FROMSYMBOL': ...,
        'HIGH24HOUR': ...,
        'LASTMARKET': ...,
        'LASTTRADEID': ...,
        'LASTUPDATE': ...,
        'LASTVOLUME': ...,
        'LASTVOLUMETO': ...,
        'LOW24HOUR': ...,
        'MARKET': ...,
        'OPEN24HOUR': ...,
        'PRICE': ...,
        'TOSYMBOL': ...,
        'TYPE': ...,
        'VOLUME24HOUR': ...,
        'VOLUME24HOURTO': ...}
```

*Example 1:*

Get all the exchanges were the LTC/EUR currency pair is available for trading.


```python
coin_data = coin.get_coin_snapshot("LTC", "EUR")
exchanges = [e['MARKET'] for e in coin_data['Exchanges']]
exchanges
```




    ['BitSquare',
     'Tidex',
     'HitBTC',
     'Kraken',
     'CCEDK',
     'Yacuna',
     'BTCE',
     'TheRockTrading',
     'Bitstamp',
     'Cexio',
     'Exmo',
     'BitBay',
     'Coinbase']



*Example 2:*

Get the aggregated trading volume across all the available exchanges for the NEO/BTC pair. 


```python
coin_data = coin.get_coin_snapshot("NEO", "BTC")
volume = float(coin_data['AggregatedData']['VOLUME24HOUR'])
volume
```




    2402094.313135109



---

### price.py

To access these functions, you can import them in the following way:


```python
from cryptocompy import price
```

---

#### get_current_price

```python
get_current_price(fsyms, tsyms, e='all', try_conversion=True, full=False, format='raw')
```

Get latest trading price or full trading information in display or raw format for the specified FROM/TO currency pairs.

*Arguments:*

* `fsyms`: Single string or list of FROM symbols.
* `tsyms`: Single string or list of TO symbols.
* `e`: Default returns average price across all exchanges. Can be set to the name of a single exchange.
* `try_conversion`: If the crypto does not trade directly into the toSymbol requested, BTC will be used for conversion. If set to false, it will try to get values without using any conversion at all.
* `full`: Default of False returns only the latest price.	
* `format`: Default returns the 'RAW' format. Can be changed to 'DISPLAY' format.

*Returns:*

Returns a dictionary containing the latest price pairs if full is set to false:

```
{fsym1: {tsym1: ..., tsym2:..., ...},
 fsym2: {...},
 ...}
```

or full trading info dictionaries for all the price pairs in the other case:

```
{fsym1: {tsym1: {'CHANGE24HOUR': ...,
                 'CHANGEPCT24HOUR': ...,
                 'FLAGS': ...,
                 'FROMSYMBOL': ...,
                 'HIGH24HOUR': ...,
                 'LASTMARKET': ...,
                 'LASTTRADEID': ...,
                 'LASTUPDATE': ..., 
                 'LASTVOLUME': ...,
                 'LASTVOLUMETO': ...,
                 'LOW24HOUR': ...,
                 'MARKET' ...,
                 'MKTCAP': ...,
                 'OPEN24HOUR': ...,
                 'PRICE': ...,
                 'SUPPLY': ...,
                 'TOSYMBOL': ...,
                 'TYPE': ..., 
                 'VOLUME24HOUR': ...,
                 'VOLUME24HOURTO': ...},
         tsym2: ..., ...},
fsym2: {...},
...}
```

*Example 1:*

Get the current BTC prices averaged across all exchanges in EUR, USD and ETH.


```python
price.get_current_price("BTC", ["EUR", "USD", "ETH"])
```




    {'BTC': {'ETH': 13.49, 'EUR': 3361.68, 'USD': 3962.38}}



*Example 2:*

Get the current BTC and ETH prices in EUR and USD.


```python
price.get_current_price(["ETH", "BTC"], ["EUR", "USD"])
```




    {'BTC': {'EUR': 3361.62, 'USD': 3962.16},
     'ETH': {'EUR': 248.04, 'USD': 293.32}}



*Example 3:*

Get the current ETH trading price in EUR from Kraken. 


```python
price.get_current_price("ETH", "EUR", e="Kraken")
```




    {'ETH': {'EUR': 247.78}}



*Example 4:*

Get the current trading information about the ETH/EUR and ETH/BTC markets.


```python
price.get_current_price("ETH", ["EUR", "BTC"], full=True)
```




    {'ETH': {'BTC': {'CHANGE24HOUR': -0.002250000000000002,
       'CHANGEPCT24HOUR': -2.945411703102503,
       'FLAGS': '4',
       'FROMSYMBOL': 'ETH',
       'HIGH24HOUR': 0.07657,
       'LASTMARKET': 'HitBTC',
       'LASTTRADEID': 39464478,
       'LASTUPDATE': 1506430531,
       'LASTVOLUME': 1.168,
       'LASTVOLUMETO': 0.08631987199999999,
       'LOW24HOUR': 0.07397,
       'MARKET': 'CCCAGG',
       'MKTCAP': 7030474.546815192,
       'OPEN24HOUR': 0.07639,
       'PRICE': 0.07414,
       'SUPPLY': 94827010.3428,
       'TOSYMBOL': 'BTC',
       'TYPE': '5',
       'VOLUME24HOUR': 304207.36878715,
       'VOLUME24HOURTO': 22841.949823297473},
      'EUR': {'CHANGE24HOUR': 4.6200000000000045,
       'CHANGEPCT24HOUR': 1.8977982254354275,
       'FLAGS': '4',
       'FROMSYMBOL': 'ETH',
       'HIGH24HOUR': 251.35,
       'LASTMARKET': 'Kraken',
       'LASTTRADEID': 1506430533.8385,
       'LASTUPDATE': 1506430533,
       'LASTVOLUME': 2,
       'LASTVOLUMETO': 495.6,
       'LOW24HOUR': 241.61,
       'MARKET': 'CCCAGG',
       'MKTCAP': 23522788185.63497,
       'OPEN24HOUR': 243.44,
       'PRICE': 248.06,
       'SUPPLY': 94827010.3428,
       'TOSYMBOL': 'EUR',
       'TYPE': '5',
       'VOLUME24HOUR': 96101.47060460004,
       'VOLUME24HOURTO': 23793339.85357493}}}



*Example 5:*

Get the current trading information about the ETH/EUR and ETH/BTC markets in 'DISPLAY' format.


```python
price.get_current_price("ETH", ["EUR", "BTC"], full=True, format="display")
```




    {'ETH': {'BTC': {'CHANGE24HOUR': 'Ƀ -0.0022',
       'CHANGEPCT24HOUR': '-2.93',
       'FROMSYMBOL': 'Ξ',
       'HIGH24HOUR': 'Ƀ 0.07657',
       'LASTMARKET': 'BitTrex',
       'LASTTRADEID': 116252205,
       'LASTUPDATE': 'Just now',
       'LASTVOLUME': 'Ξ 1',
       'LASTVOLUMETO': 'Ƀ 0.07420',
       'LOW24HOUR': 'Ƀ 0.07397',
       'MARKET': 'CryptoCompare Index',
       'MKTCAP': 'Ƀ 7,031.45 K',
       'OPEN24HOUR': 'Ƀ 0.07639',
       'PRICE': 'Ƀ 0.07415',
       'SUPPLY': 'Ξ 94,827,318.3',
       'TOSYMBOL': 'Ƀ',
       'VOLUME24HOUR': 'Ξ 304,262.6',
       'VOLUME24HOURTO': 'Ƀ 22,846'},
      'EUR': {'CHANGE24HOUR': '€ 4.68',
       'CHANGEPCT24HOUR': '1.92',
       'FROMSYMBOL': 'Ξ',
       'HIGH24HOUR': '€ 251.35',
       'LASTMARKET': 'Gatecoin',
       'LASTTRADEID': 46923452,
       'LASTUPDATE': 'Just now',
       'LASTVOLUME': 'Ξ 13.29',
       'LASTVOLUMETO': '€ 3,304.96',
       'LOW24HOUR': '€ 241.61',
       'MARKET': 'CryptoCompare Index',
       'MKTCAP': '€ 23.53 B',
       'OPEN24HOUR': '€ 243.44',
       'PRICE': '€ 248.12',
       'SUPPLY': 'Ξ 94,827,318.3',
       'TOSYMBOL': '€',
       'VOLUME24HOUR': 'Ξ 96,114.8',
       'VOLUME24HOURTO': '€ 23,796,644.8'}}}



---

#### get_current_trading_info

```python
get_current_trading_info(fsym, tsym, markets='all', try_conversion=True, format='raw)
```

Get the latest trading info of the requested pair as a volume weighted average across the markets requested.

*Arguments:*

* `fsym`: FROM symbol.
* `tsym`: TO symbol.
* `markets`: List containing the market names. Default returns average across all markets. If only a single market is specified, the function will also return the full aggregate.
* `try_conversion`: If the crypto does not trade directly into the toSymbol requested, BTC will be used for conversion. If set to false, it will try to get values without using any conversion at all.
* `format`: Default returns the 'RAW' format. Can be set to 'DISPLAY' format.

*Returns:*

The returned latest average trading information dictionary contains the following key value pairs:

```
{'PRICE': ...,
'LASTVOLUMETO': ...,
'TOSYMBOL': ...,
'LOW24HOUR': ...,
'CHANGE24HOUR': ...,
'FROMSYMBOL': ...,
'FLAGS': ...,
'VOLUME24HOUR': ...,
'HIGH24HOUR': ...,
'LASTUPDATE': ...,
'VOLUME24HOURT': ...,
'LASTMARKET': ...,
'CHANGEPCT24HOUR': ...,
'OPEN24HOUR': ...,
'MARKET': ...,
'LASTTRADEID': ...,
'LASTVOLUME': ...}
```

*Example 1:*

Get current trading information about the BTC/USD pair across all markets.


```python
price.get_current_trading_info("BTC", "USD")
```




    {'BTC': {'USD': {'CHANGE24HOUR': 178.78999999999996,
       'CHANGEPCT24HOUR': 4.725418783268755,
       'FLAGS': 0,
       'FROMSYMBOL': 'BTC',
       'HIGH24HOUR': 3993.76,
       'LASTMARKET': 'CCCAGG',
       'LASTTRADEID': 21336459,
       'LASTUPDATE': 1506430583,
       'LASTVOLUME': 1.513e-05,
       'LASTVOLUMETO': 0.05983915,
       'LOW24HOUR': 3772.63,
       'MARKET': 'CUSTOMAGG',
       'OPEN24HOUR': 3783.58,
       'PRICE': 3962.37,
       'TOSYMBOL': 'USD',
       'VOLUME24HOUR': 98845.786925876,
       'VOLUME24HOURTO': 387191231.031879}}}



*Example 2:*

Obtain the trading information aggregated for Poloniex, Kraken and Coinbase in display format.


```python
price.get_current_trading_info("BTC", "USD", markets=["Poloniex", "Kraken", "Coinbase"], format='display')
```




    {'BTC': {'USD': {'CHANGE24HOUR': '$ 179.75',
       'CHANGEPCT24HOUR': '4.76',
       'FROMSYMBOL': 'Ƀ',
       'HIGH24HOUR': '$ 3,990.9',
       'LASTMARKET': 'Coinbase',
       'LASTTRADEID': 21336465,
       'LASTUPDATE': 'Just now',
       'LASTVOLUME': 'Ƀ 0.00000252',
       'LASTVOLUMETO': '$ 0.009967',
       'LOW24HOUR': '$ 3,765.99',
       'MARKET': 'CUSTOMAGG',
       'OPEN24HOUR': '$ 3,776.3',
       'PRICE': '$ 3,956.05',
       'TOSYMBOL': '$',
       'VOLUME24HOUR': 'Ƀ 20,430.5',
       'VOLUME24HOURTO': '$ 79,891,717.1'}}}



---

#### get_day_average_price

```python
get_day_average_price(fsym, tsym, e='all', try_conversion=True, avg_type='HourVWAP', utc_hour_diff=0)
```

Get the current days average price of a currency pair.

*Arguments:*

* `fsym`: FROM symbol.
* `tsym`: TO symbol.
* `e`: Default returns average price across all exchanges. Can be set to the name of a single exchange.
* `try_conversion`: If the crypto does not trade directly into the toSymbol requested, BTC will be used for conversion. If set to false, it will try to get values without using any conversion at all.
* `avg_type`: 'HourVWAP' returns a volume weighted average of the hourly close price. The other option 'MidHighLow' gives the average between the 24 hour high and low.
* `utc_hour_diff`: Pass hour difference to UTC for different time zone.

*Returns:*

Returns a price dictionairy containing the current days average price as float.

```
{fsym: {tsym: price}}
```

*Example 1:*

Get the current days ETH/EUR average price across all exchanges.


```python
price.get_day_average_price("ETH", "EUR")
```




    {'ETH': {'EUR': 247.4}}



*Example 2:*

Get the MidHighLow price for the DGB/XLM pair in the UTC-8 time zone. 


```python
price.get_day_average_price("DGB", "XLM", avg_type="MidHighLow", utc_hour_diff=-8)
```




    {'DGB': {'XLM': 1.17}}



---

#### get_historical_eod_price

```python
get_historical_eod_price(fsym, tsyms, date, e='all', try_conversion=True)
```

Get end of day price for cryptocurrency in any other currency for the requested timestamp.

*Arguments:*

* `fsym`: FROM symbol.
* `tsyms`: Single string or list of TO symbols.
* `date`: Date as string with these formats: "Y-m-d", "Y-m-d H-M-S".Date as string with this format: "Y-m-d H-M-S".
* `e`: Default returns average price across all exchanges. Can be set to the name of a single exchange.
* `try_conversion`: If the crypto does not trade directly into the toSymbol requested, BTC will be used for conversion. If set to false, it will try to get values without using any conversion at all.

*Returns:*

Returns a dictionary containing the end of day price pairs for the provided date.

```
{fsym: {tsym1: ..., tsym2: ..., ...}}
```

*Example 1:*

Get the end of day price from April 20, 2017 for DASH in USD.


```python
price.get_historical_eod_price("DASH", "USD", "2017-04-20 00:00:00")
```




    {'DASH': {'USD': 72.34}}



*Example 2:*

Obtain the end of day price of LTC in BTC and EUR from Kraken on the 23rd of July in 2017.


```python
price.get_historical_eod_price("LTC", ["BTC", "EUR"], "2017-07-23", e="Kraken")
```




    {'LTC': {'BTC': 0.0165, 'EUR': 40.03}}



---

#### get_historical_data

```python
get_historical_data(fsym, tsym, freq, info='full', e='all', try_conversion=True, aggregate=1, 
                    limit=1440, to_ts=False)
```

Get minute-by-minute historical price and volume information for the requested currency pair. Available data is limited to the last 7 days.

*Arguments:*

* `fsym`: FROM symbol.
* `tsym`: TO symbol.
* `info`: Select price or volume information to return. Default of 'full' returns all of them. Can be set to 'high', 'low', 'open', 'close', 'volumefrom', and 'volumeto' or a list containing several of those values.
* `e`: Default returns average price across all exchanges. Can be set to the name of a single exchange.
* `try_conversion`: If the crypto does not trade directly into the toSymbol requested, BTC will be used for conversion. If set to false, it will try to get values without using any conversion at all.
* `aggregate`: Aggregates the minute prices into bins of the specified size.
* `limit`: Number of minute prices. The limit settings depend on the freq selected. Using aggregate reduces the maximum number of points that can be returned by a factor equal to the chosen bin size.
               minute: default = 1440, min = 1, max = 2000
               hour: default = 168, min = 1, max 2000
               day: default = 30, min = 1, max 2000	

*Returns:*

List of dictionairies containing the price and volume information for each requested tick.

```
[{'time': ..., 'close': ..., 'high': ..., 'low': ..., 'open': ...,
  'volumefrom': ..., 'volumeto': ...},
  {...},
 ...]
```

*Example 1:*

Get full price and volume data for the last five 5-minute segments.


```python
price.get_historical_data('BTC', 'USD', 'minute', aggregate=5, limit=5)
```




    [{'close': 3968.35,
      'high': 3970.96,
      'low': 3966.42,
      'open': 3969,
      'time': '2017-09-26 14:30:00',
      'volumefrom': 180.86,
      'volumeto': 718660.5},
     {'close': 3963.65,
      'high': 3968.88,
      'low': 3962.33,
      'open': 3968.35,
      'time': '2017-09-26 14:35:00',
      'volumefrom': 218.48000000000002,
      'volumeto': 867707.4900000001},
     {'close': 3968.23,
      'high': 3969.23,
      'low': 3961.76,
      'open': 3963.65,
      'time': '2017-09-26 14:40:00',
      'volumefrom': 318.74,
      'volumeto': 1265744.9000000001},
     {'close': 3967.88,
      'high': 3970.84,
      'low': 3966.82,
      'open': 3968.23,
      'time': '2017-09-26 14:45:00',
      'volumefrom': 214.83999999999997,
      'volumeto': 856669.6699999999},
     {'close': 3961.98,
      'high': 3967.88,
      'low': 3961.22,
      'open': 3967.88,
      'time': '2017-09-26 14:50:00',
      'volumefrom': 338.34,
      'volumeto': 1344325.82},
     {'close': 3961.65,
      'high': 3962.84,
      'low': 3961.57,
      'open': 3961.98,
      'time': '2017-09-26 14:55:00',
      'volumefrom': 101.10000000000001,
      'volumeto': 400661.15}]



*Example 2:*

Get the ETH/USD trading volume in ETH for the last ten minutes.


```python
price.get_historical_data('ETH', 'USD', 'minute', info='volumefrom', aggregate=1, limit=10)
```




    [{'time': '2017-09-26 14:50:00', 'volumefrom': 102.89},
     {'time': '2017-09-26 14:51:00', 'volumefrom': 323.75},
     {'time': '2017-09-26 14:52:00', 'volumefrom': 113.72},
     {'time': '2017-09-26 14:53:00', 'volumefrom': 79.65},
     {'time': '2017-09-26 14:54:00', 'volumefrom': 136.11},
     {'time': '2017-09-26 14:55:00', 'volumefrom': 45.03},
     {'time': '2017-09-26 14:56:00', 'volumefrom': 147.95},
     {'time': '2017-09-26 14:57:00', 'volumefrom': 169.3},
     {'time': '2017-09-26 14:58:00', 'volumefrom': 69.73},
     {'time': '2017-09-26 14:59:00', 'volumefrom': 18.81},
     {'time': '2017-09-26 15:00:00', 'volumefrom': 0}]



*Example 3:*

Get the XRP closing prices in USD for the last ten days.


```python
price.get_historical_data('XRP', 'USD', 'day', info='close', aggregate=1, limit=10)
```




    [{'close': 0.1828, 'time': '2017-09-16 02:00:00'},
     {'close': 0.1814, 'time': '2017-09-17 02:00:00'},
     {'close': 0.1933, 'time': '2017-09-18 02:00:00'},
     {'close': 0.1848, 'time': '2017-09-19 02:00:00'},
     {'close': 0.1817, 'time': '2017-09-20 02:00:00'},
     {'close': 0.171, 'time': '2017-09-21 02:00:00'},
     {'close': 0.1728, 'time': '2017-09-22 02:00:00'},
     {'close': 0.1791, 'time': '2017-09-23 02:00:00'},
     {'close': 0.1757, 'time': '2017-09-24 02:00:00'},
     {'close': 0.1846, 'time': '2017-09-25 02:00:00'},
     {'close': 0.186, 'time': '2017-09-26 02:00:00'}]



---

### mining.py

To access these functions, you can import them in the following way:


```python
from cryptocompy import mining
```

---

#### get_mining_contracts

```python
get_mining_contracts()
```

Get all the mining contracts information available.

*Returns:*

This function returns two major dictionaries. The first one contains information about the coins for which mining contracts data is available.

`coin_data`: 

```
{symbol1: {'BlockNumber': ...,
           'BlockReward': ...,
           'BlockRewardReduction': ...,
           'BlockTime': ...,
           'DifficultyAdjustment': ...,
           'NetHashesPerSecond': ...,
           'PreviousTotalCoinsMined': ...,
           'PriceUSD': ...,
           'Symbol': ...,
           'TotalCoinsMined': ...},
 symbol2: {...},
 ...}
```

The other one contains all the available mining contracts.

`mining_data`: 

```
{id1: {'AffiliateURL': ...,
       'Algorithm': ...,
       'Company': ...,
       'ContractLength': ...,
       'Cost': ...,
       'CurrenciesAvailable': ...,
       'CurrenciesAvailableLogo': ...,
       'CurrenciesAvailableName': ...,
       'Currency': ...,
       'FeePercentage': ...,
       'FeeValue': ...,
       'FeeValueCurrency': ...,
       'HashesPerSecond': ...,
       'Id': id1,
       'LogoUrl': ...,
       'Name': ...,
       'ParentId': ...,
       'Recommended': ...,
       'Sponsored': ...,
       'Url': ...},
 id2: {...},
 ...}

```

*Example 1:*

Get the symbols of all the coins for which mining contracts information is available.


```python
coin_data, _ = mining.get_mining_contracts()

sorted(list(coin_data.keys()))
```




    ['BCH', 'BTC', 'DASH', 'ETC', 'ETH', 'LTC', 'XMR', 'ZEC']



*Example 2:*

Calculate the average cost of all contracts available for LTC.


```python
_, mining_data = mining.get_mining_contracts()

costs = []
for id, c in mining_data.items():
    if c['CurrenciesAvailable'] == 'LTC':
        costs.append(float(c['Cost']))

avg_cost = sum(costs) / len(costs)
avg_cost
```




    1630.4142857142856



---

#### get_mining_equipment

```python
get_mining_equipment()
```

Get all the mining equipment information available.

*Returns:*

This function returns two major dictionaries. The first one contains information about the coins for which mining equipment data is available.

`coin_data`: 

```
{symbol1: {'BlockNumber': ...,
           'BlockReward': ...,
           'BlockRewardReduction': ...,
           'BlockTime': ...,
           'DifficultyAdjustment': ...,
           'NetHashesPerSecond': ...,
           'PreviousTotalCoinsMined': ...,
           'PriceUSD': ...,
           'Symbol': ...,
           'TotalCoinsMined': ...},
 symbol2: {...},
 ...}
```

The other one contains all the available mining equipment.

`mining_data`:

```
{id1: {'AffiliateURL': ...,
       'Algorithm': ...,
       'Company': ...,
       'Cost': ...,
       'CurrenciesAvailable': ...,
       'CurrenciesAvailableLogo': ...,
       'CurrenciesAvailableName': ...,
       'Currency': ...,
       'EquipmentType': ...,
       'HashesPerSecond': ...,
       'Id': ...,
       'LogoUrl': ...,
       'Name': ...,
       'ParentId': ...,
       'PowerConsumption': ...,
       'Recommended': ...,
       'Sponsored': ...,
       'Url': ...},
 id2: {...},
 ...}
```

*Example 1:*

Get the different equipment categories that are present.


```python
_, mining_data = mining.get_mining_equipment()

equipment_types = set()
for id, m in mining_data.items():
    equipment_types.add(m['EquipmentType'])

equipment_types = sorted(list(equipment_types))
equipment_types
```




    ['ASIC', 'Chip', 'GPU', 'Refurbished GPU', 'Rig', 'Rig Bundle', 'USB']



---

### rest.py
* AllExchanges() (unfinished)

---

### top.py

To access these functions, you can import them in the following way:


```python
from cryptocompy import top
```

---

#### get_top_exchanges

```python
get_top_exchanges(fsym, tsym, limit=5)
```

Get top exchanges by 24 hour trading volume for the currency pair.

*Arguments:*

* fsym: FROM symbol.
* tsym: TO symbol.
* limit: Number of results. Default value returns top 5 exchanges.

*Returns:*

Function returns a list containing a dictionary for each result:

```
[{'exchange': ..., 'fromSymbol': ..., 'toSymbole': ..., ''volume24h': ..., 'volume24hTo': ...}, 
 {...}, 
 ...]
```

The list is ordered based on the volume of the FROM currency starting with the highest value.

*Example 1:*

Return the five exchanges with the highest BTC/EUR trading volumes.


```python
top.get_top_exchanges('BTC', 'EUR')
```




    [{'exchange': 'Kraken',
      'fromSymbol': 'BTC',
      'toSymbol': 'EUR',
      'volume24h': 8351.092083899992,
      'volume24hTo': 27628317.082228173},
     {'exchange': 'Bitstamp',
      'fromSymbol': 'BTC',
      'toSymbol': 'EUR',
      'volume24h': 2568.1894343999998,
      'volume24hTo': 8511824.021590795},
     {'exchange': 'Coinbase',
      'fromSymbol': 'BTC',
      'toSymbol': 'EUR',
      'volume24h': 1517.8138159200014,
      'volume24hTo': 5048021.616161475},
     {'exchange': 'Gatecoin',
      'fromSymbol': 'BTC',
      'toSymbol': 'EUR',
      'volume24h': 1168.84521697,
      'volume24hTo': 3863339.3599144304},
     {'exchange': 'Quoine',
      'fromSymbol': 'BTC',
      'toSymbol': 'EUR',
      'volume24h': 732.7815031599999,
      'volume24hTo': 2408914.8726677545}]



---

#### get_top_coins

```python
get_top_coins(tsym, limit=20)
```

Get top coins by 24 hour trading volume value in the requested currency.

*Arguments:*

* tsym: TO symbol.
* limit: Number of results. Default value returns top 20 coins.

*Returns:*

Function returns a list containing a dictionary for each result:

```
[{'SUPPLY': ..., 'SYMBOL': ..., 'VOLUME24HOURTO': ...}, 
 {...}, 
 ...]
```

The list is ordered based on the volume of the TO currency starting with the highest value.

*Example 1:*

Find the five coins with the highest 24h trading volume in EUR.


```python
top.get_top_coins('EUR', limit=5)
```




    [{'SUPPLY': 16588012, 'SYMBOL': 'BTC', 'VOLUME24HOURTO': 49837171.97736684},
     {'SUPPLY': 94827328.3116,
      'SYMBOL': 'ETH',
      'VOLUME24HOURTO': 23263552.251434967},
     {'SUPPLY': 53106307.3718871,
      'SYMBOL': 'LTC',
      'VOLUME24HOURTO': 4445373.437819645},
     {'SUPPLY': 38305873865,
      'SYMBOL': 'XRP',
      'VOLUME24HOURTO': 1309229.1452122403},
     {'SUPPLY': 16617575, 'SYMBOL': 'BCH', 'VOLUME24HOURTO': 1104153.3960400792},
     {'SUPPLY': 7582684.8248937,
      'SYMBOL': 'DASH',
      'VOLUME24HOURTO': 484580.27885076427}]



---

#### get_top_pairs

```python
get_top_pairs(fsym, limit=5)
```

Get top trading pairs by 24 hour aggregated volume for a currency.

*Arguments:*

* fsym: FROM symbol.
* limit: Number of results. Default value returns top 5 pairs.

*Returns:*

Function returns a list containing a dictionary for each result:

```
[{'exchange': ..., 'fromSymbol': ..., 'toSymbol': ..., 'volume24h': ..., 'volume24hTo': ...}, 
 {...}, 
 ...]
```

The list is ordered based on the volume of the FROM currency starting with the highest value.

*Example 1:*

Get the five currencies with the highest BTC trading volumes.


```python
pair_data = top.get_top_pairs('BTC')
tsyms = [p['toSymbol'] for p in pair_data]
tsyms
```




    ['JPY', 'USD', 'KRW', 'CNY', 'EUR']


