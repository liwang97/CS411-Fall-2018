import requests
from flask import Flask, render_template, request, jsonify, json


app = Flask(__name__)


@app.route("/")
def home():
	return render_template("home.html")

@app.route('/', methods = ["GET", 'POST'])
def test():

	form =  request.form["answer"]

	url = "http://archive.org/services/search/v1/scrape"
	querystring = {"fields":"title" , "sorts" :"date desc","q":form, "court": 100}
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

	return str1


if __name__ == "__main__":
    app.run(debug=True)

