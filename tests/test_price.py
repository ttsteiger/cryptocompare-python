import pytest

from tests.cryptocompy_vcr import cryptocompy_vcr

from cryptocompy import price


@cryptocompy_vcr.use_cassette()
def test_get_full_current_price():

    res = price.get_current_price("BTC", "USD", full=True)

    assert res['BTC']['USD']
    btc_price = res['BTC']['USD']

    assert btc_price['TYPE'] == '5'
    assert btc_price['MARKET'] == 'CCCAGG'
    assert btc_price['FROMSYMBOL'] == 'BTC'
    assert btc_price['TOSYMBOL'] == 'USD'
    assert btc_price['FLAGS'] == '4'
    assert btc_price['PRICE'] == 6593.57
    assert btc_price['LASTUPDATE'] == 1538255360
    assert btc_price['LASTVOLUME'] == 0.01861566
    assert btc_price['LASTVOLUMETO'] == 122.3979645
    assert btc_price['LASTTRADEID'] == '51692673'
    assert btc_price['VOLUMEDAY'] == 34753.13910881231
    assert btc_price['VOLUMEDAYTO'] == 228196363.20126274
    assert btc_price['VOLUME24HOUR'] == 36811.604030178525
    assert btc_price['VOLUME24HOURTO'] == 241927684.9410378
    assert btc_price['OPENDAY'] == 6635.4
    assert btc_price['HIGHDAY'] == 6635.42
    assert btc_price['LOWDAY'] == 6474.23
    assert btc_price['OPEN24HOUR'] == 6652.5
    assert btc_price['HIGH24HOUR'] == 6663.43
    assert btc_price['LOW24HOUR'] == 6472.26
    assert btc_price['LASTMARKET'] == 'Coinbase'
    assert btc_price['CHANGE24HOUR'] == -58.93000000000029
    assert btc_price['CHANGEPCT24HOUR'] == -0.8858323938369078
    assert btc_price['CHANGEDAY'] == -41.82999999999993
    assert btc_price['CHANGEPCTDAY'] == -0.6304066069867669
    assert btc_price['SUPPLY'] == 17295637
    assert btc_price['MKTCAP'] == 114039993254.09
    assert btc_price['TOTALVOLUME24H'] == 183347.3560109875
    assert btc_price['TOTALVOLUME24HTO'] == 1208121423.1291404


@cryptocompy_vcr.use_cassette()
def test_get_display_current_price():

    res = price.get_current_price("BTC", "USD", full=True, format='display')
    assert res['BTC']['USD']
    btc_price = res['BTC']['USD']

    assert btc_price['PRICE'] == '$ 6,591.28'
    assert btc_price['LASTUPDATE'] == 'Just now'
    assert btc_price['MKTCAP'] == '$ 114.01 B'


@cryptocompy_vcr.use_cassette()
@pytest.mark.parametrize("fsim", [
    "BTC",
    ["BTC"],
    ["BTC", "ETH"],
])
@pytest.mark.parametrize("tsim", [
    "USD",
    ["USD"],
    ["USD", "EUR"],
])
def test_get_current_price_inputs(fsim, tsim):

    prices = price.get_current_price(fsim, tsim)

    assert "BTC" in prices.keys()

    btc_prices = prices['BTC']

    assert 'USD' in btc_prices.keys()


@cryptocompy_vcr.use_cassette()
def test_get_current_trading_info():
    trading_infos = price.get_current_trading_info("BTC", "USD")
    assert trading_infos

    assert 'BTC' in trading_infos.keys()
    btc_trading_infos = trading_infos['BTC']

    assert 'USD' in btc_trading_infos.keys()
    assert btc_trading_infos['USD']['PRICE'] == 6593.74
    assert btc_trading_infos['USD']['FROMSYMBOL'] == 'BTC'
    assert btc_trading_infos['USD']['TOSYMBOL'] == 'USD'
    assert btc_trading_infos['USD']['MARKET'] == 'CUSTOMAGG'


@cryptocompy_vcr.use_cassette()
def test_get_display_trading_info():

    trading_infos = price.get_current_trading_info("BTC", "USD",
                                                   format='display')
    assert trading_infos['BTC']['USD']
    btc_trading_infos = trading_infos['BTC']['USD']

    assert btc_trading_infos['PRICE'] == '$ 6,595.14'
    assert btc_trading_infos['LASTUPDATE'] == 'Just now'


@cryptocompy_vcr.use_cassette()
def test_get_day_average_price():
    day_average = price.get_day_average_price('BTC', 'USD')

    assert 'BTC' in day_average
    btc_average = day_average['BTC']

    assert 'USD' in btc_average
    assert btc_average['USD'] == 6546.84


@cryptocompy_vcr.use_cassette()
def test_get_historical_eod_price():
    eod_prices = price.get_historical_eod_price('BTC', 'USD',
                                                "2018-01-01 00:00:00")

    assert 'BTC' in eod_prices
    btc_eod_price = eod_prices['BTC']

    assert btc_eod_price['USD'] == 6552.28


@cryptocompy_vcr.use_cassette()
def test_get_historical_data():

    datas = price.get_historical_data('BTC', 'USD', 'minute')

    assert len(datas) == 1441

    data = datas[0]
    data['time'] == '2018-09-29 00:30:00'
    data['close'] == 6655.97
    data['high'] == 6655.99
    data['low'] == 6655.58
    data['open'] == 6655.99
    data['volumefrom'] == 5.21
    data['volumeto'] == 34791.94


@cryptocompy_vcr.use_cassette()
def test_get_high_historical_data():

    datas = price.get_historical_data('BTC', 'USD', 'minute', info='high')

    data = datas[0]
    assert data.keys() == set(['time', 'high'])
    data['time'] == '2018-09-29 00:30:00'
    data['high'] == 6537.44


@cryptocompy_vcr.use_cassette()
def test_get_current_price_with_invalid_pair():
    """
        In this test, the pair "ETH-USD" doesn't exist on Binance
    """

    prices = price.get_current_price("ETH", ["BTC", "USD"],
                                     full=False, e="Binance")

    assert prices == {'ETH': {'BTC': 0.03184}}


@cryptocompy_vcr.use_cassette(record_mode="new")
def test_get_current_price_with_invalid_pair_full():
    """
        In this test, the pair "ETH-USD" doesn't exist on Binance
    """

    prices = price.get_current_price("ETH", ["BTC", "USD"],
                                     full=True, e="Binance")

    assert prices == {'ETH': {'BTC': {'CHANGE24HOUR': 0.0035700000000000037,
                                      'CHANGEDAY': 0.0023350000000000037,
                                      'CHANGEPCT24HOUR': 12.25120109814689,
                                      'CHANGEPCTDAY': 7.687242798353921,
                                      'FLAGS': '2',
                                      'FROMSYMBOL': 'ETH',
                                      'HIGH24HOUR': 0.033245,
                                      'HIGHDAY': 0.033245,
                                      'HIGHHOUR': 0.032955,
                                      'IMAGEURL': '/media/20646/eth_logo.png',
                                      'LASTTRADEID': '111733607',
                                      'LASTUPDATE': 1558018109,
                                      'LASTVOLUME': 0.037,
                                      'LASTVOLUMETO': 0.00121027,
                                      'LOW24HOUR': 0.029022,
                                      'LOWDAY': 0.030319,
                                      'LOWHOUR': 0.031921,
                                      'MARKET': 'Binance',
                                      'MKTCAP': 3470296.1605699365,
                                      'OPEN24HOUR': 0.02914,
                                      'OPENDAY': 0.030375,
                                      'OPENHOUR': 0.031953,
                                      'PRICE': 0.03271,
                                      'SUPPLY': 106092820.5616,
                                      'TOSYMBOL': 'BTC',
                                      'TOTALVOLUME24H': 20795810.484037984,
                                      'TOTALVOLUME24HTO': 679281.7414301885,
                                      'TYPE': '2',
                                      'VOLUME24HOUR': 713119.1569999984,
                                      'VOLUME24HOURTO': 22376.90812277601,
                                      'VOLUMEDAY': 483148.6399999981,
                                      'VOLUMEDAYTO': 15535.450436684,
                                      'VOLUMEHOUR': 29999.47499999993,
                                      'VOLUMEHOURTO': 975.9747860490053}}}
