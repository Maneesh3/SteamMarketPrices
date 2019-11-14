import json					# json extract
import urllib.request
import re					# regular expressions
import urllib.parse
#from bs4 import beautifulSoup

# currency ID = 24 for INR

CurrencyID = 24

def getListLinks():
	f = open("list.txt", "r")
	f1 = f.readlines()
	return f1


def main():
	listLinks = getListLinks()
	for llink in listLinks:
		try:
			appId = re.search('listings/(.+?)/', str(llink)).group(1)
		except AttributeError:
			appId = ''
			print('appID error !')
		
		try:
			productNameUrl = llink.split(appId+'/')[1]
		except:
			productNameUrl = ''
			print('productName error !')
			
		#print(appId + "      " + productNameUrl)

		url = 'https://steamcommunity.com/market/priceoverview/?appid=' + appId + '&currency=' + str(CurrencyID) + '&market_hash_name=' + productNameUrl

		productName = urllib.parse.unquote(llink).split(appId+'/')[1]
		print(productName)

		response = urllib.request.urlopen(url)
		data = json.loads(response.read())
		print(data['lowest_price'])
		
		

if 	__name__=="__main__":
	main()
