
from runstats import Statistics
import math
import csv

if (__name__ == '__main__'):
	# Outline:
	inputData = []
	with open('data/btc_xlm_thirtyMin.csv', 'r') as f:
		reader = csv.DictReader(f)
		for line in reader:
			toType = {
				'O': float(line['O']),
				'C': float(line['C']),
				'H': float(line['H']),
				'L': float(line['L'])
				#'V': float(line['V']),
				#'T': line['T'],
				#'BV': float(line['BV'])
			}
			inputData.append(toType)

	data = [float(x['C']) for x in inputData]

	# Calculate log of each return to form series
	series = []
	for (t, x) in enumerate(data[:-1], start=1):
		r_t = math.log(data[t]/data[t-1])
		series.append(r_t)

	#print (series)

	stats = Statistics()
	for x in series:
		stats.push(x)

	# Test kurtosis and skewness

	# Skewness < 0 indicates large decreases after many small gains, skewness > 0 indicates large gains after many small losses
	# Optimally want -0.8 < x < 0, or x > 1
	print('skewness: ', stats.skewness())

	# Kurtosis we want to be leptokurtic (> average)
	print('kurtosis: ', stats.kurtosis())

	# TODO Jarque-Bera about normal distribution - pref want not a normal distribution (ie reject H0 / p-value ~= 0)

	# TODO time series tests



	# Evaluate trading over time inputdata (not the log series)
	# TODO, shorting??
	start = 1000
	isBought = False
	isInitial = True
	initialTradePrice = 1
	current = start 
	mintick = 0.00000001 # Minimum tick
	totalTrades = -1

	# TODO replace 'C' with some form of better notation of average?
	for (t, x) in enumerate(inputData[:-1], start=1):
		if (not isBought and inputData[t]['C'] >= inputData[t-1]['H'] + mintick):
			isBought = True

			# Sell short
			if (not isInitial):
				#print('sell short, buy long', t, current,
				#      initialTradePrice, inputData[t]['C'])
				current = (initialTradePrice/inputData[t]['C'])*current
				totalTrades += 1

			# Buy new
			initialTradePrice = inputData[t]['C']
			isInitial = False


		if (isBought and inputData[t]['C'] <= inputData[t-1]['L'] - mintick):
			isBought = False

			# Sell long
			#print('sell long, buy short', t, current,
			#      initialTradePrice, inputData[t]['C'])
			current = (inputData[t]['C']/initialTradePrice)*current
			totalTrades += 1

			# Short new
			initialTradePrice = inputData[t]['C']

	#if(isBought):
	#	current = (inputData[-1]['OC']/initialTradePrice)*current
	print('samples, trades, amount: ', len(inputData), totalTrades, current)
