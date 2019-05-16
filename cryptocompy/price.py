from deepmerge import always_merger
# price.py

from .helper_functions import build_url, load_data, timestamp_to_date, \
date_to_timestamp


def get_current_price(fsyms, tsyms, e='all', try_conversion=True, full=False,
                      format='raw'):
    """Get latest trading price or full trading information in display or raw
    format for the specified FROM/TO currency pairs.

    Args:
        fsyms: Single string or list of FROM symbols.
        tsyms: Single string or list of TO symbols.
        e: Default returns average price across all exchanges.
           Can be set to the name of a single exchange.
        try_conversion: If the crypto does not trade directly into the toSymbol
            requested, BTC will be used for conversion.
            If set to false, it will try to get values
            without using any conversion at all.
        full: Default of False returns only the latest price. True returns the
            following dictionary structure containing the full trading info:
        format: Default returns the 'RAW' format. Can be set to 'DISPLAY'
            format.
    Returns:
        Returns a dictionary containing the latest price pairs
        if full is set to false:

        {fsym1: {tsym1: ..., tsym2:..., ...},
         fsym2: {...},
         ...}

        or full trading info dictionaries for all the price pairs in the other
        case:

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
    """

    # select API function based on 'full' parameter value
    if not full:
        func = 'pricemulti'
    else:
        func = 'pricemultifull'

    # convert single fsym and tsym input to single element lists
    if not isinstance(fsyms, list):
        fsyms = [fsyms]
    if not isinstance(tsyms, list):
        tsyms = [tsyms]

    # load data
    data = {}
    for tsym in tsyms:
        url = build_url(func, fsyms=fsyms, tsyms=[tsym], e=e,
                        try_conversion=try_conversion)
        pair_data = load_data(url)
        if pair_data.get('Response') == 'Error':
            continue
        data = always_merger.merge(data, pair_data)

    #  select right format to return for full requests
    if full and format == 'raw':
        data = data['RAW']
    elif full and format == 'display':
        data = data['DISPLAY']

    return data


def get_current_trading_info(fsym, tsym, markets='all', try_conversion=True,
                       		 format='raw'):
	"""
	Get the latest trading info of the requested pair as a volume weighted
	average based on the markets requested.
	
	Args:
		fsym: FROM symbol.
		tsym: TO symbol.
		markets: List containing the market names.
		try_conversion: If the crypto does not trade directly into the toSymbol
			requested, BTC will be used for conversion. If set to false, it will
			try to get values without using any conversion at all.
		format: Default returns the 'RAW' format. Can be set to 'DISPLAY'
			format.

	Returns:
		The returned latest average trading information dictionary contains
		the following key value pairs:
		
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
	"""
	
	# load data
	url = build_url('generateAvg', fsym=fsym, tsym=tsym, markets=markets,
	                try_conversion=try_conversion)
	data = load_data(url)

	# select format to return
	if format == 'raw':
		data = data['RAW']
	elif format == 'display':
		data = data['DISPLAY']

	return {fsym: {tsym: data}}


def get_day_average_price(fsym, tsym, e='all', try_conversion=True,
                    	  avg_type='HourVWAP', utc_hour_diff=0):
	"""
	Get the current days average price of a currency pair.

	Args:
		fsym: FROM symbol.
		tsym: TO symbol.
		e: Default returns average price across all exchanges. Can be set to the
			name of a single exchange.
		try_conversion: If the crypto does not trade directly into the toSymbol
			requested, BTC will be used for conversion. If set to false, it will
			try to get values without using any conversion at all.
		avg_type: 'HourVWAP' returns a volume weighted average of the hourly
			close price. The other option 'MidHighLow' gives the average between
			the 24 hour high and low.
		utc_hour_diff: Pass hour difference to UTC for different time zone.

		# add 'toTs' parameter
		######################
		######################
		######################
		######################
		######################
		######################
	
	Returns:
		Returns a price dictionairy containing the current days average price as
		float.

		{fsym: {tsym: price}}
	"""

	# load data
	url = build_url('dayAvg', fsym=fsym, tsym=tsym, e=e,
	                try_conversion=try_conversion, avg_type=avg_type,
	                utc_hour_diff=utc_hour_diff)
	data = load_data(url)

	# remove 'ConversionType' information
	del data['ConversionType']
	
	return {fsym: data}


def get_historical_eod_price(fsym, tsyms, date, e='all', try_conversion=True):
	"""Get end of day price for cryptocurrency in any other currency for the
	requested timestamp.

	Args:
		fsym: FROM symbol.
		tsyms: Single string or list of TO symbols.
		date: Date as string with this format: "Y-m-d H:M:S".
		e: Default returns average price across all exchanges. Can be set to the
			name of a single exchange.
		try_conversion: If the crypto does not trade directly into the toSymbol
			requested, BTC will be used for conversion. If set to false, it will
			try to get values without using any conversion at all.

	Returns:
		Returns a dictionary containing the end of day price pairs for the
		provided date.
		
		{fsym: {tsym1: ..., tsym2: ..., ...}}
	"""

	# convert single fsym and tsym input to single element lists
	if not isinstance(tsyms, list):
		tsyms = [tsyms]

	# convert date to timestamp
	ts = date_to_timestamp(date)

	# load data
	url = build_url("pricehistorical", fsym=fsym, tsyms=tsyms, ts=ts,
	                e=e, try_conversion=try_conversion)
	data = load_data(url)

	return data


def get_historical_data(fsym, tsym, freq, info='full', e='all',
                        try_conversion=True, aggregate=1, limit=1440,
                        to_ts=False):
	"""Get minute-by-minute historical price and volume information for
	the requested currency pair. Available data is limited to the last 7 days.
	
	Args:
		fsym: FROM symbol.
		tsym: TO symbol.
		freq: Frequency of the data. Can be set to 'minute', 'hour' or 'day'.
		info: Select price or volume information to return. Default of 'full'
			returns all of them. Can be set to 'high', 'low', 'open', 'close',
			'volumefrom', and 'volumeto' or a list containing several of those
			values.
		e: Default returns average price across all exchanges. Can be set to the
		   name of a single exchange.
		try_conversion: If the crypto does not trade directly into the toSymbol
			requested, BTC will be used for conversion. If set to false, it will
			try to get values without using any conversion at all.
		aggregate: Aggregates the minute prices into bins of the specified size.
		limit: Number of minute prices. The limit settings depend on the freq
			selected:
				minute: default = 1440, min = 1, max = 2000
				hour: default = 168, min = 1, max 2000
				day: default = 30, min = 1, max 2000
			
			Using aggregate reduces the maximum number of points that can be
			returned by a factor equal to the chosen bin size.
		
		# add 'toTs' parameter
		######################
		######################
		######################
		######################
		######################
		######################
	
	Returns:
		List of dictionairies containing the price and volume information for
		each requested tick.

		[{'time': ..., 'close': ..., 'high': ..., 'low': ..., 'open': ...,
		  'volumefrom': ..., 'volumeto': ...},
		  {...},
		 ...]
	"""

	# load data
	url = build_url(freq, fsym=fsym, tsym=tsym, freq=freq, e=e,
	                try_conversion=try_conversion, aggregate=aggregate,
	                limit=limit, to_ts=to_ts)
	data = load_data(url)
	data = data['Data']

	# convert timestamps to nice date format
	for d in data:
		d['time'] = timestamp_to_date(d['time'])

	# convert single input info to single element list
	if not isinstance(info, list):
		info = [info]

	# select information to return
	if info[0] == 'full':
		return data
	else:
		for d in data:
			for k, v in list(d.items()):
				if k not in info and k != 'time':
					del d[k]
				
		return data
