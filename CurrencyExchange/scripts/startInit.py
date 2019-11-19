import requests
from bs4 import BeautifulSoup
import json
def startInit():
	retryTimes = 0
	while True:
		try:
			r=requests.get("https://www.kuaiyilicai.com/bank/rmbfx/b-safe.html",headers={"user-agent":"Chrome/76"},timeout=5)
			r.raise_for_status()
			r.encoding=r.apparent_encoding
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
			demo=r.text
			soup=BeautifulSoup(demo,"html.parser")
			with open("../data/currencyShort.json", "w+") as f:
				a="{\"人民币\":\"CNY\""
				for i in range(1, len(soup.table.find_all('tr'))):
					a+=",\""+str(soup.table.find_all('tr')[i].find_all('td')[0].div.next_sibling.strip().split(' ')[0].strip())+"\":\""+str(soup.table.find_all('tr')[i].find_all('td')[0].div.next_sibling.strip().split(' ')[-1].strip().strip('(').strip(')'))+"\""
				a+="}"
				json.dump(json.loads(a), f)
		break