# Hub.py 枢纽脚本文件

import os
import sys
from difflib import SequenceMatcher	#用于比较字符串相似度进行猜词

import Commands

def checkCmdSet(cmdSet, inputCmd):
	for i in cmdSet.split(' '):
		if i == inputCmd.lower():
			return True
	return False

class CurrencyHubException(Exception):
	reason = ''
	def __init__(self):
		pass

	def __init__(self, reason:str):
		self.reason = reason

	def getReason(self):
		return self.reason

class CommandNotFoundException(CurrencyHubException):
	pass

# 猜词
def maybeItIs(cmdname):
	for i in Commands.genericCmds:
		if i[2][1] != -1 or interactive:
			for j in i[0].split(' '):
				seq = SequenceMatcher(None, cmdname.lower(), j.lower())
				if seq.ratio() > 0.65:
					return j

def invalidCmdRes(exception:CurrencyHubException, cmdArg:str):
	print('{0}: '.format(type(exception).__name__), end = '')
	print(exception.getReason())
	guess = maybeItIs(cmdArg)
	if guess != None:
		print('Did you mean "{0}"?'.format(guess))

# 读取系统参数
def loadArgs(From):
	args = []
	if From < 0:
		From = 0
	for i in range(From, len(sys.argv)):
		args.append(sys.argv[i])
	return args

# Action Manager
def actionManager(actionList):
	if len(actionList) >= 2:
		if actionList[1] <= 0:
			if len(actionList) > 2:
				if not interactive:
					actionList[0]()
				else:
					actionList[2]()
			else:
				actionList[0]()
		else:
			if interactive or len(sys.argv) - 2 < actionList[1]:
				if not interactive:
					print('Too few arguments')
				if len(actionList) > 2:
					actionList[2]()
				return
			actionList[0](loadArgs(2))

def actionMatcher():
	for i in Commands.genericCmds:
		if i[2][1] != -1 or interactive:
			if checkCmdSet(i[0], cmdArg):
				actionManager(i[2])
				return
	raise CommandNotFoundException('"{0}" is not a command.'.format(cmdArg))

# 匹配操作
def matchActions():
	try:
		actionMatcher()
	except CommandNotFoundException as e:
		invalidCmdRes(e, cmdArg)

interactive = False # 是否在交互模式下

global cmdArg

if __name__ == '__main__':
	if len(sys.argv) == 1:
		interactive = True
		# ---------------- Interactive Mode ----------------- #
		cmdLineNum = 1
		Commands.initialize()
		while True:
			cmdArg = input('cmd:{0:03}> '.format(cmdLineNum))
			cmdLineNum += 1
			if cmdArg == '':
				continue
			
			# Match actions
			matchActions()
			print()
	else:
		# ------------------ Shell Mode --------------------- #
		cmdArg = sys.argv[1]
		matchActions()
		print()
