import requests
from flask import Flask, render_template, request, jsonify, json
import pymongo
from pymongo import MongoClient


app = Flask(__name__)


@app.route("/")
def home():
	return render_template("home.html")

@app.route('/', methods = ["GET", 'POST'])
def test():


	client = MongoClient()
	db = client.db
	collection1 = db.test_database
	# db.dropCollection("collection1")

	form =  request.form["answer"]

	k = collection1.find_one({"search_term" : form})

	if (k != None):
		str0 = "from database"
		str0 += "<br/>"
		items = k['result']
		str0 += items
		return str0

	else:

		url = "http://archive.org/services/search/v1/scrape"
		querystring = {"fields":"title" , "sorts" :"num_reviews desc","q":form, "count": 100}
		headers = {
	    	# '': "",
	    		'cache-control': "no-cache",
	    		'Postman-Token': "fde1a0c5-c63c-480c-ac8c-c358810466a3"
	    		}

		response = requests.request("GET", url, headers=headers, params=querystring)

		json_data = response.json()
		items = json_data['items']
		str1 = ""
		for item in items:
			str1 += str(item['title']) 
			str1 += "<br/>"

		result = {"search_term" : form,
					"result" : str1,

		}

		collection1.insert_one(result)

		return str1


if __name__ == "__main__":
    app.run(debug=True)

