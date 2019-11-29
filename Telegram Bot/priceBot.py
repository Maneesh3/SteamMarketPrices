import json
import requests
import time
import urllib
import re

from dbHandler import DBHandler

def getToken():
		f = open("config.json","r")
		dat = json.load(f)
		return dat['telegram_Bot_Token']

def getDBConfig():
		f = open("config.json","r")
		dat = json.load(f)
		return dat['cluster_name'],dat["dataBase_name"]

cName, dbName = getDBConfig()
db = DBHandler(cName,dbName)

TOKEN = getToken()
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

commands = {'/links':'display all the links','/chcur':'change the default currency','/add <link>':'provide link to save in database for price retrive'}


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def check_url(link):
	retList = ['0','ERROR_PROG','AppID','ProductID','URL','JSON']
	ret = get_price(link)
	if(ret in [1,2,3,4,5]):
		return retList[ret]
	return 1

def get_price(llink):
	try:
		appId = re.search('listings/(.+?)/', str(llink)).group(1)
	except AttributeError:
		appId = ''
		return 2
		
	try:
		productNameUrl = llink.split(appId+'/')[1]
	except:
		productNameUrl = ''
		return 3
			
	#print(appId + "      " + productNameUrl)

	url = 'https://steamcommunity.com/market/priceoverview/?appid=' + appId + '&currency=' + str(24) + '&market_hash_name=' + productNameUrl

	productName = urllib.parse.unquote(llink).split(appId+'/')[1]
	print(productName)
	try:
		response = urllib.request.urlopen(url)
		data = json.loads(response.read())
	except:
		return 4

	try:
		return (data['lowest_price'])
	except KeyError:
		print("JSON error")
		return 5
		
	return 1

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def handle_updates(updates):
	for update in updates["result"]:
		text = update["message"]["text"]
		chat = update["message"]["chat"]["id"]
		name = update["message"]["from"]["first_name"]

        #items = db.get_items(chat)
        # if text == "/done":
        #     #keyboard = build_keyboard(items)
        #     #send_message("Select an item to delete", chat, keyboard)
        #     print("done")
		if text == "/start":
			send_message("Welcome to Steam Market Prices BOT, which retrives prices of items on Steam market", chat)
			if(db.check_user(chat) == 0):
				send_message("Adding user into database",chat)
				send_message("Check out the commands using - /help ",chat)
				db.add_user(chat,name,24)
		elif text == "/help":
			helpList = [k + " :  " + v for k,v in commands.items()]
			msgHelp = "\n".join(helpList)
			send_message(msgHelp, chat)
                    # return the commands !
		elif text.startswith("/add "):
			addLink = text[5:]
			retCheck = check_url(addLink)
			
			if(retCheck != 1):
				send_message("Error occured,check URL, : "+ retCheck,chat)			
			else:
				print(retCheck)
				#db.add_link(chat,addLink)
		elif text == "/links":
			linksList = db.get_links(chat)
			msgLinks = "\n".join(linksList)
			send_message(msgLinks, chat)
		# elif text in items:
		# 	db.delete_item(text, chat)
		# 	items = db.get_items(chat)
		# 	keyboard = build_keyboard(items)
		# 	send_message("Select an item to delete", chat, keyboard)
		else:
			send_message("I couldn't get that darling", chat)
            


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)


def main():
    #db('SteamMarketPrices','test2')
	last_update_id = None
	while True:
		updates = get_updates(last_update_id)					# getting prev request [MUST CHECK]
		if len(updates["result"]) > 0:
			last_update_id = get_last_update_id(updates) + 1
			handle_updates(updates)
		time.sleep(0.5)


if __name__ == '__main__':
	main()