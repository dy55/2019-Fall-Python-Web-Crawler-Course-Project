# currencyKit.MiscUtils
# MiscUtils.py 杂项工具库

import json

import startInit

class CurrencyNameKit:
	def CnToShort(name, output = True):
		try:
			f = open('../data/currencyShort.json', 'r')
			f.close()
		except:
			startInit.startInit()
		finally:
			with open('../data/currencyShort.json', 'r+') as f:
				nameSet = json.load(f)
				try:
					shortName = nameSet[name]
				except:
					if output:
						print('Not Found')
					return 'Not Found'
				else:
					if output:
						print(shortName)
					return shortName

	def ShortToCn(shortName, output = True):
		try:
			f = open('../data/currencyShort.json', 'r')
			f.close()
		except:
			startInit.startInit()
		finally:
			with open('../data/currencyShort.json', 'r+') as f:
				nameSet = json.load(f)
				for i in nameSet:
					if nameSet[i] == shortName.upper():
						if output:
							print(i)
						return i
			if output:
				print('Not Found')
			return 'Not Found'
