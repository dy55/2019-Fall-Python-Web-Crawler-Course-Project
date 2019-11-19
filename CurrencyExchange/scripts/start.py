# start.py 启动脚本文件

import os
import re
import startInit

def checkDotnet():
	print('Checking the status of .NET Core')
	result = os.popen('dotnet --version').read()
	if re.search('^\d+.\d+.\d+$', result):
		return True
	return False

def startUI():
	os.popen(r'dotnet ..\netcoreapp3.0\CurrencyUI.dll')

def initialize():
	startInit.startInit()

def startOperation():
	if checkDotnet():
		print('This computer has installed .NET Core or .NET Framework.')
		print('Initializing...')
		initialize()
		print('Initializing completed')
		print('Trying to run the interface...')
		startUI()
	else:
		print('This computer has not installed .NET Core or .NET Framework.')

if __file__ == '__main__':
	startOperation()