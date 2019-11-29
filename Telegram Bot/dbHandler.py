import pymongo
import json
from pymongo import MongoClient

class DBHandler:
	
	def __init__(self, clusNme,dbNme):
		self.cluster = MongoClient(self.getAddr())
		self.mydb = self.cluster[clusNme]
		self.mycol = self.mydb[dbNme]

	def getAddr(self):
		f = open("config.json","r")
		dat = json.load(f)
		return dat['mongoDB']
	
	def add_user(self, chatID, name, curNo):
		doc = {"name":name,"chatID":chatID,"curNo": curNo,"links":[]}
		x = self.mycol.insert_one(doc)

	def add_link(self, chatID, link):
		find = {"chatID":chatID}
		for x in self.mycol.find(find):
			tempLinksList = x["links"]
			tempLinksList.append(link)
			self.mycol.update_one({"chatID":chatID}, {"$set":{"links":tempLinksList}})
			return

	def check_user(self, chatID):
		find = {"checkID":chatID}
		if(self.mycol.count(find) == 0):
			return 0
		else:
			return 1	

	def delete_link(self, chatID, num):
		find = {"chatID":chatID}
		for x in self.mycol.find(find):
			tempLinksList = x["links"]
			tempLinksList.remove(tempLinksList[num])
			self.mycol.update_one({"chatID":chatID}, {"$set":{"links":tempLinksList}})
			return
		

	def get_links(self, chatID):
		find = {"chatID":chatID}
		for x in self.mycol.find(find):
			return x["links"]
			