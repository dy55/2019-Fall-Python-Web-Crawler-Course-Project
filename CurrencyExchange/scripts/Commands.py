import sys

import currencyKit
from currencyKit import CurrencyStatistics
from currencyKit import CurrencyTrend
from currencyKit import MiscUtils
import start

# 通用命令组 动作类型 0: 无直接参数, >0: 有直接参数, -1: 交互模式动作
genericCmds = (
	# Commands, Description, Generic actions => (Default action, Action Type, [Alternative action])
	('help -h /h hello', 'Get Help', [lambda: help(), 0]),
	('startgui startui -u /u', 'Run Currency GUI', [lambda: start.startOperation(), 0]),
	('rate -r /r', 'Get exchange rate', [lambda args: exchangeRateShell(args), 2, lambda: exchangeRateOp()]),
	('stat -s /s', 'Get statistics of each currency to CNY', [lambda: CurrencyStatistics.getStat(), 0]),
	('visualstat vstat -vs /vs', 'Get visual statistics of each currency to CNY', [lambda: exStat(), 0, lambda: CurrencyStatistics.visualStat(choose('Save the picture of figure?'))]),
	('trend -t /t', 'Get specific trend of exchange rate of currency to CNY', [lambda args: CurrencyTrend.trend(args[0]), 1, lambda: CurrencyTrend.trend(input('From: '))]),
	('visualtrend vtrend -vt /vt', 'Get specific visual trend of exchange rate of currency to CNY', [lambda args: exTrend(args), 1, lambda: CurrencyTrend.visualTrend(input('From: '), saveFig=choose('Save the figure picture?'))]),
	('short -sh /sh', 'Get currency name for short by its Chinese name', [lambda args: MiscUtils.CurrencyNameKit.CnToShort(args[0]), 1, lambda: MiscUtils.CurrencyNameKit.CnToShort(input('CN Name: '))]),
	('cnname -cn /cn', 'Get Chinese name of currency by its short name', [lambda args: MiscUtils.CurrencyNameKit.ShortToCn(args[0]), 1, lambda: MiscUtils.CurrencyNameKit.ShortToCn(input('Short Name: '))]),
	('exit -e', 'Exit from the hub', [lambda: exitHub(), -1])
	)

# 交互模式初始化
def initialize():
	help()

def choose(prompt):
	while True:
		choice = input('{0} (y/n): '.format(prompt))
		if choice.lower() == 'y':
			return True
		elif choice.lower() == 'n':
			return False

# 特别函数集合

def help():
	print('\n------------- Help ----------------')
	print('Welcome to Exchange Command Hub!')
	print()
	print('Commands we support:')
	for i in range(len(genericCmds)):
		print('{0:<30}\t{1}'.format(genericCmds[i][0], genericCmds[i][1]))
	print('-----------------------------------')

# Shell Operation Functions
# Exchange rate function
def exchangeRateShell(args):
	if len(args) == 2:
		CurrencyStatistics.getExchangeRate(args[0], args[1])
	elif len(args) == 3:
		CurrencyStatistics.getExchangeRate(args[0], args[1], float(args[2]))
	else:
		exchangeRateOp()

# Visual Stat
def exStat():
	if len(sys.argv) < 3:
		CurrencyStatistics.visualStat()
	else:
		if sys.argv[3] == '--dns' or sys.argv[3] == 'donotsave':
			CurrencyStatistics.visualStat(False)
		else:
			CurrencyStatistics.visualStat()

# Visual Trend
def exTrend(args):
	if len(args) == 2:
		if args[1] == '--dns' or args[1] == 'donotsave':
			CurrencyTrend.visualTrend(args[0], False)
		else:
			CurrencyTrend.visualTrend(args[0])
	elif len(args) == 1:
		CurrencyTrend.visualTrend(args[0])

# Interactive Operation Functions
# Exchange rate function
def exchangeRateOp():
	arg2 = input('From: ')
	arg3 = input('To: ')
	amount = input('Amount: ')
	if amount != '':
		amount = float(amount)
		CurrencyStatistics.getExchangeRate(arg2, arg3, amount)
	else:
		CurrencyStatistics.getExchangeRate(arg2, arg3)

# Exit function
def exitHub(code = 0):
	print('Exiting...')
	sys.exit(code)

# ----------------------- #

