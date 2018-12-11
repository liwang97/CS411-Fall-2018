# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 06:04:43 2018

@author: chris
"""

import requests
from flask import Flask, render_template, request, jsonify, json
import pymongo
from pymongo import MongoClient
import collections
import bson
import pprint
app = Flask(__name__)


@app.route("/")
def home():
	return render_template("home.html")

client = MongoClient()
db = client.db
users = db.test_database
collection1 = db.test_database3
collection2 = db.test_database2

"""
db.create_collection("userdb",{
    validator: { $jsonSchema: {
            bsonType: "object",
            required: ["uid", "favorites"]
            properties: {
                    uid: {
                        bsonType: "string",
                        Description: "String id of the user, required"
                        },
                    favorites: {
                            bsonType: "array",
                            Description: "array of favorite songs, not required"
                            }
                    }   
                }
            }
        }
    )
"""
def hasaccount(userid):
    useriddb = users.find_one({"uid": userid});
    if userid == useriddb:
        return useriddb
    else: 
        users.insert_one({"uid": userid, "favorites":[]});
        return userid
    
def addfavorites(userid, add):
    user = users.find_one({"uid": userid})
    array = user["favorites"]
    array.append(add)
    users.update_one(
            { "uid": userid },
            { "$set": { "favorites": array } }
            );
    
def remfavorites(userid, rem):
    users.update_one(
            { "uid": userid },
            { "$pull": { "favorites": rem } }
            );

def showfavorites(userid):
    user = users.find_one({"uid": userid}, {"favorites"})
    return user["favorites"]

def showusers():
    user = collection2.find_one()
    return user["uid"]
def insertuser(userid):
    collection2.insert_one({"uid": userid});


# if __name__ == '__main__':
#collection2.drop()
#users.drop()
# hasaccount("ada")
# # addfavorites("cjhuang", "testing123")
# addfavorites("ada", "grateful dead")
# #pprint.pprint(users.find_one({"uid":"ada"}))
# # remfavorites("cjhuang", "grateful dead")
pprint.pprint(users.find_one({"uid":"one"}))
# addfavorites("ada", "testing123")
# addfavorites("ada", "grateful dead")
# # # #print(users)
# pprint.pprint(collection2.find_one())
print(collection2.find_one())
print(collection1.find_one())
print(showfavorites("one"))
# pprint.pprint(showusers())


