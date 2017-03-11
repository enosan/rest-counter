#!/bin/python
from pymongo import MongoClient
from constants import USERS_DOC, EMAIL, PASSWORD

client = MongoClient()

def _getDocument(name):
	db = client.restCounter
	return db[name]

def existUser(email):
	doc = _getDocument(USERS_DOC)
	return doc.find({ EMAIL: email }).count() > 0

def passwordMatch(email, pw):
	doc = _getDocument(USERS_DOC)
	for user in doc.find({ EMAIL: email }):
		return user[PASSWORD] == pw
			
def insertUser(email, passwordHash):
	doc = _getDocument(USERS_DOC)
	doc.insert_one({
		EMAIL: email,
		PASSWORD: passwordHash
	})

	