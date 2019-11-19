# currencyKit.CurrencyTrend
# CurrencyTrend.py 汇率趋势函数库

import requests
from bs4 import BeautifulSoup
import matplotlib as mpl
from matplotlib import pyplot as plt
import yaml
import datetime

def trend(fromCurrency, writeAsYaml = False, output = True):
	retryTimes = 0
	while True:
		try:
			r = requests.get('https://www.kuaiyilicai.com/huilv/d-safe-{0}.html'.format(fromCurrency.lower()), timeout=5)
			r.raise_for_status()
		except requests.exceptions.Timeout as tout:
			if retryTimes <= 5:
				print('Failed to access the site. The program will try again. (Remain {0} times)'.format(5 - retryTimes))
				print('(Exception: {0})'.format(tout))
				retryTimes += 1
				continue
			else:
				print('Failed to access the site. The program has stopped.')
				print('(Exception: {0})'.format(tout))
				return
		except Exception as e:
			print('Failed to access the site. The program has stopped.')
			print('(Exception: {0})'.format(e))
			return
		else:
			soup = BeautifulSoup(r.text, 'html.parser')
			briefDataList = {
				'涨跌': soup.find_all('table')[0].find_all('tr')[0].find_all('td')[1].span.string,
				'最高': soup.find_all('table')[0].find_all('tr')[1].find_all('td')[1].span.string,
				'最低': soup.find_all('table')[0].find_all('tr')[2].find_all('td')[1].span.string,
				'平均': soup.find_all('table')[0].find_all('tr')[3].find_all('td')[1].span.string
			}

			if output:
				for i in briefDataList:
					print(i)
					print(briefDataList[i].split(' ')[0].strip())
					print(briefDataList[i].split(' ')[1].strip().strip('(').strip(')'))
				print()

			firstLine = True
			dataSet = []
			for i in soup.find_all('table')[-1].find_all('tr'):
				if firstLine:
					firstLine = not firstLine
					continue
				Date = i.find_all('td')[0].string
				middle = float(i.find_all('td')[1].span.string)
				rate = i.find_all('td')[2].string
				each1000 = float(i.find_all('td')[-1].find_all('span')[-1].string.strip())
				dataBlock = {str(Date): {'middle': str(middle), 'rate': str(rate), 'each1000': str(each1000)}}
				dataSet.insert(0, dataBlock)
				if output:
					print(Date)
					print(middle)
					print(rate)
					print(each1000)
			if writeAsYaml:
				with open('../data/trend.yml', 'w+') as f:
					yaml.dump(dataSet, f)
		break

def visualTrend(fromCurrency, saveFig = False, showGraph = True):
	trend(fromCurrency, writeAsYaml=True, output=False)
	try:
		f = open('../data/trend.yml', 'r')
		dataList = yaml.load_all(f, Loader=yaml.FullLoader)
	except:
		return
	values = []
	dates = []
	for i in dataList:
		for j in i:
			for k in j:
				values.append(float(j[k]['middle']))
				dates.append(k)
	f.close()

	mpl.rcParams['font.family'] = 'DengXian'
	fig = plt.figure()
	plt.plot(dates, values, color='green')
	plt.title('趋势统计')
	plt.xticks(rotation=45, fontsize='8')
	plt.ylabel('汇率（CNY / {0}）'.format(fromCurrency.upper()))
	plt.xlabel('日期')
	if showGraph:
		plt.show()
	if saveFig:
		fig.savefig('../data/exTrend-{0}-{1:%Y-%m-%d}.png'.format(fromCurrency.upper(), datetime.date.today()))