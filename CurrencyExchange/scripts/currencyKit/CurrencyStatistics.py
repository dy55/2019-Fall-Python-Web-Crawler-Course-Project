# currencyKit.CurrencyStatistics
# CurrencyStatistics.py 汇率统计函数库

import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import yaml
import datetime

from currencyKit import MiscUtils

def getStat(output = True, yamlFile = False):
	retryTimes = 0
	while True:
		try:
			r = requests.get('https://www.kuaiyilicai.com/bank/rmbfx/b-safe.html', timeout=5)
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
			if yamlFile:
				f = open('../data/exchangeData.yaml', 'w+')
			for i in range(1, len(soup.table.find_all('tr'))):
				infoList = {
						str(soup.table.find_all('tr')[i].find_all('td')[0].div.next_sibling.strip().split(' ')[0].strip()):[
						str(soup.table.find_all('tr')[i].find_all('td')[0].div.next_sibling.strip().split(' ')[-1].strip().strip('(').strip(')')),
						str(soup.table.find_all('tr')[i].find_all('td')[1].string)
						]
					}
				if output:
					for i in infoList:
						print(i)
					for i in infoList.values():
						for j in i:
							print(j)
				if yamlFile:
					yaml.dump(infoList, f)
		break

def getExchangeRate(From, To, amount=100):
	From = From.upper()
	To = To.upper()
	if MiscUtils.CurrencyNameKit.ShortToCn(From, False) == 'Not Found' or MiscUtils.CurrencyNameKit.ShortToCn(To, False) == 'Not Found':
		print('Invalid Currency Name')
		return
	retryTimes = 0
	while True:
		try:
			r = requests.get('http://qq.ip138.com/hl.asp', params={'from': From.upper(), 'to': To.upper(), 'q': str(amount)}, timeout=5)
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
			r.encoding = r.apparent_encoding
			soup = BeautifulSoup(r.text, 'html.parser')
			rate = float(soup.table.find_all('tr')[2].find_all('td')[1].p.string)
			amountRate = amount * rate
			print(amountRate)
			print('1 {1} = {0} {2}'.format(rate, From, To))
		break

def visualStat(saveFig = True):
	getStat(False, True)
	names = []
	values = []
	with open('../data/exchangeData.yaml', 'r') as f:
		data = yaml.load_all(f, Loader=yaml.FullLoader)
		for i in data:
			for j in i:
				names.append('{0} {1}'.format(j, i[j][0]))
				values.append(float(i[j][1]))
	fig = plt.figure()
	mpl.rcParams['font.family'] = 'DengXian'
	plt.bar(names, values, color='red')
	plt.title('汇率概览')
	plt.xticks(rotation=45, fontsize=7)
	plt.xlabel('货币')
	plt.yticks(np.arange(0, max(values) * 1.1, 0.5))
	plt.ylabel('折合人民币')
	plt.show()
	if saveFig:
		fig.savefig('../data/stat-{0:%Y-%m-%d}.png'.format(datetime.date.today()))
