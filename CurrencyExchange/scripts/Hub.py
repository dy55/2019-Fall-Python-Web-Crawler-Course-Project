# Hub.py 枢纽脚本文件

import os
import sys
from difflib import SequenceMatcher	#用于比较字符串相似度进行猜词

import currencyKit
from currencyKit import CurrencyStatistics
from currencyKit import CurrencyTrend
from currencyKit import MiscUtils
import start

# 命令集元组
cmds = (
		'help -h /h hello',
		'stat -s /s',
		'rate -r /r',
		'startgui startui -u /u',
		'visualstat vstat -vs /vs',
		'trend -t /t',
		'visualtrend vtrend -vt /vt',
		'short -sh /sh',
		'cnname -cn /cn'
	)

# 命令描述元组
description = (
		'Get Help',
		'Get statistics of each currency to CNY',
		'Get exchange rate',
		'Run Currency GUI',
		'Get visual statistics of each currency to CNY',
		'Get specific trend of exchange rate of currency to CNY',
		'Get specific visual trend of exchange rate of currency to CNY',
		'Get currency name for short by its Chinese name',
		'Get Chinese name of currency by its short name'
	)

def checkCmdSet(cmdSet, inputCmd):
	for i in cmdSet.split(' '):
		if i == inputCmd.lower():
			return True
	return False

# 猜词
def maybeItIs(cmdname):
	for i in cmds:
		for j in i.split(' '):
			seq = SequenceMatcher(None, cmdname.lower(), j.lower())
			if seq.ratio() > 0.65:
				return j

def help():
	print('\n-----------------------------------')
	print('Welcome to Exchange Query Hub!')
	print('-----------------------------------')
	print('There are the commands we support:')
	for i in range(len(cmds)):
		print(f'{cmds[i]:<30}\t{description[i]}')
	print('{0:<30}\tExit from the Hub'.format('exit'))
	print('-----------------------------------')

def choose(prompt):
	while True:
		choice = input('{0} (y/n): '.format(prompt))
		if choice.lower() == 'y':
			return True
		elif choice.lower() == 'n':
			return False

# Interactive Operation Functions
def exchangeRateOp():
	arg2 = input('From: ')
	arg3 = input('To: ')
	amount = input('Amount: ')
	if amount != '':
		amount = float(amount)
		CurrencyStatistics.getExchangeRate(arg2, arg3, amount)
	else:
		CurrencyStatistics.getExchangeRate(arg2, arg3)

if __name__ == '__main__':
	if len(sys.argv) == 1:
		# Interactive Mode
		cmdLineNum = 1
		help()
		while True:
			cmdArg = input('cmd({0:03})> '.format(cmdLineNum))
			cmdLineNum += 1
			if cmdArg == '':
				continue
			if cmdArg.lower() == 'exit':		# exit
				print('Exiting...')
				sys.exit(0)
			if checkCmdSet(cmds[0], cmdArg):	# help
				help()
			elif checkCmdSet(cmds[1], cmdArg):	# stat
				CurrencyStatistics.getStat()
			elif checkCmdSet(cmds[2], cmdArg):	# rate
				exchangeRateOp()
			elif checkCmdSet(cmds[3], cmdArg):	# startgui
				start.startOperation()
			elif checkCmdSet(cmds[4], cmdArg):	# visualstat
				CurrencyStatistics.visualStat(choose('Save the picture of figure?'))
			elif checkCmdSet(cmds[5], cmdArg):	# trend
				CurrencyTrend.trend(input('From: '))
			elif checkCmdSet(cmds[6], cmdArg):	# visualtrend
				CurrencyTrend.visualTrend(input('From: '), saveFig=choose('Save the figure picture?'));
			elif checkCmdSet(cmds[7], cmdArg):	# short
				MiscUtils.CurrencyNameKit.CnToShort(input('CN Name: '))
			elif checkCmdSet(cmds[8], cmdArg):	# cnname
				MiscUtils.CurrencyNameKit.ShortToCn(input('Short Name: '))
			else:								# other
				print('Unknown Command "{0}"'.format(cmdArg))
				guess = maybeItIs(cmdArg)
				if guess != None:
					print('Did you mean "{0}"?'.format(guess))
			print()

	# Shell Mode
	cmdArg = sys.argv[1]

	if checkCmdSet(cmds[0], cmdArg):		# help
		help()
	elif checkCmdSet(cmds[1], cmdArg):		# stat
		currencyKit.CurrencyStatistics.getStat()
	elif checkCmdSet(cmds[2], cmdArg):		# rate
		if len(sys.argv) >= 5:
			amount = float(sys.argv[4])
			currencyKit.CurrencyStatistics.getExchangeRate(sys.argv[2], sys.argv[3], amount)
		elif len(sys.argv) == 4:
			currencyKit.CurrencyStatistics.getExchangeRate(sys.argv[2], sys.argv[3])
		else:
			print('Too few arguments')
			exchangeRateOp()
	elif checkCmdSet(cmds[3], cmdArg):		# startgui
		start.startOperation()
	elif checkCmdSet(cmds[4], cmdArg):		# visualstat
		if len(sys.argv) > 2 and sys.argv[2] == 'donotsave':
			currencyKit.CurrencyStatistics.visualStat(False)
		else:
			currencyKit.CurrencyStatistics.visualStat(True)
	elif checkCmdSet(cmds[5], cmdArg):		# trend
		if len(sys.argv) < 3:
			print('Too few arguments')
			CurrencyTrend.trend(input('From: '))
		else:
			CurrencyTrend.trend(sys.argv[2])
	elif checkCmdSet(cmds[6], cmdArg):		# visualtrend
		if len(sys.argv) < 3:
			print('Too few arguments')
			CurrencyTrend.visualTrend(input('From: '), saveFig=choose('Save the figure picture?'))
		elif len(sys.argv) >= 4 and sys.argv[3] == 'donotsave':
			CurrencyTrend.visualTrend(sys.argv[2], saveFig=False)
		else:
			CurrencyTrend.visualTrend(sys.argv[2])
	elif checkCmdSet(cmds[7], cmdArg):		# short
		if len(sys.argv) < 3:
			print('Too few arguments')
			MiscUtils.CurrencyNameKit.CnToShort(input('CN Name: '))
		else:
			MiscUtils.CurrencyNameKit.CnToShort(sys.argv[2])
	elif checkCmdSet(cmds[8], cmdArg):		# cnname
		if len(sys.argv) < 3:
			print('Too few arguments')
			MiscUtils.CurrencyNameKit.ShortToCn(input('Short Name: '))
		else:
			MiscUtils.CurrencyNameKit.ShortToCn(sys.argv[2])
	else:									# other
		print('Unknown Command "{0}"'.format(cmdArg))
		guess = maybeItIs(cmdArg)
		if guess != None:
			print('Did you mean "{0}"?'.format(guess))
