import requests
from flask import Flask, render_template, request, jsonify, json
import pymongo
from pymongo import MongoClient
import favoritesdb as fdb

app = Flask(__name__)


@app.route("/" ,methods=["GET", "POST"])
def start():

	if 'favorite' in request.form:
				formz =  fdb.collection1.find_one()
				form = formz["search_term"]
				form2 = form + " collection Gratefuldead"
				url2 = "https://archive.org/advancedsearch.php"

				querystring2 = {"q":form2,"fl[]":"title","sort[]":"avg_rating desc","rows":"50","output":"json","sort%5B%5D":"avg_rating+desc","fl%5B%5D":"title"}

				payload2 = ""
				headers2 = {
				    # '': "",
				    'Content-Type': "application/x-www-form-urlencoded",
				    'Host': "archive.org",
				    'X-Amz-Date': "20181211T003114Z",
				    'Authorization': "AWS4-HMAC-SHA256 Credential=KydbldiyWljf1Opg/20181211/us-east-1/execute-api/aws4_request, SignedHeaders=;cache-control;content-type;host;postman-token;x-amz-date, Signature=7357829dea815dab998a0a030987942fbfbd572992a7144c854ed66b4c2c15b9",
				    'cache-control': "no-cache",
				    'Postman-Token': "a1f5f84f-a961-41d3-b9f7-1a3ada8660de"
				    }

				response2 = requests.request("GET", url2, data=payload2, headers=headers2, params=querystring2)


				json_data2 = response2.json()

				result2 = json_data2['response']
				result2 = result2['docs']

				identifier_str2 = []

				for item in result2:
					items = item['title']
					identifier_str2.append(items)

				album=identifier_str2[0]
				nickn=fdb.showusers()
				fdb.addfavorites(nickn, album)
	return render_template("login2.html")
@app.route("/profile", methods=['GET','POST'])
def profile():

	if "submitted" in request.form:
		userid=request.form["nickname"]
		fdb.collection2.drop()
		fdb.collection2.insert_one({"uid":userid})
		fdb.hasaccount(userid)
		lst=fdb.showfavorites(userid)
		return render_template("profile.html", filename=lst)
	else:
		return render_template("errorProfile.html")
		#s = ['song1', 'song2', 'song3']
		# return render_template("login2.html") #, filename = ls)


@app.route('/home', methods = ["GET", 'POST'])
def home():
	# if 'answer' in request.form:
	# if request.args.get('nickname'):
	# 	userid=request.form["nickname"]
	# 	nickn=userid
	# 	fdb.hasaccount(userid)
	# 	lst=fdb.showfavorites(userid)
	# 	return render_template("login2.html", filename=lst)
	# else:
	if "answer" in request.form:
		form =  request.form["answer"]
		form2 = form + " collection Gratefuldead"

		#form3 = request.form

		client = MongoClient()
		db = client.db
		collection1 = db.test_database
		k = fdb.collection1.find_one({"search_term" : form})
		#collection1.drop()

		if (k != None):

			return render_template("audio_track.html", identifier_str = k['num_ident'][0],lyrics =k['lyrics'])
		# if (False):
		# 	return ""

		else:

		url = "https://archive.org/advancedsearch.php"

		querystring = {"q":form2,"fl[]":"identifier","sort[]":"avg_rating desc","rows":"50","output":"json","sort%5B%5D":"avg_rating+desc","fl%5B%5D":"identifier"}

		payload = ""
		headers = {
		    # '': "",
		    'Content-Type': "application/x-www-form-urlencoded",
		    'Host': "archive.org",
		    'X-Amz-Date': "20181211T003114Z",
		    'Authorization': "AWS4-HMAC-SHA256 Credential=KydbldiyWljf1Opg/20181211/us-east-1/execute-api/aws4_request, SignedHeaders=;cache-control;content-type;host;postman-token;x-amz-date, Signature=7357829dea815dab998a0a030987942fbfbd572992a7144c854ed66b4c2c15b9",
		    'cache-control': "no-cache",
		    'Postman-Token': "a1f5f84f-a961-41d3-b9f7-1a3ada8660de"
		    }

		response = requests.request("GET", url, data=payload, headers=headers, params=querystring)


		json_data = response.json()

		result = json_data['response']
		result = result['docs']

		identifier_str = []

		for item in result:
			items = item['identifier']
			identifier_str.append(items)

		# identifier_str = str(identifier_str)
			# str1 += "<br/>"

			# str1 += response.text 

		url = "https://api.musixmatch.com/ws/1.1/matcher.lyrics.get"

		querystring = {"q_track":form,"q_artist":"Grateful%20Dead","apikey":"10529e38b136e8a39601eb86e2a8771d"}

		payload = ""
		headers = {
		    'cache-control': "no-cache",
		    'Postman-Token': "5b201c20-b1d2-4bae-b5e2-5f3d79697a9e"
		    }

		response = requests.request("GET", url, data=payload, headers=headers, params=querystring)


		if str(response.json()['message']['header']['status_code']) == "200":

			json_data_ = response.json()
			lyrics = response.json()['message']['body']['lyrics']['lyrics_body']
				# str1 += response.text

			result = {"search_term" : form,
				  "num_ident" : identifier_str[0],
				  "lyrics" : lyrics
			}

			fdb.collection1.drop()
			fdb.collection1.insert_one(result)
			

			
			
				# 	print(nickn+"helllllllo")
			# if((nickn != None) and (album  != None)):
			# 	return render_template("audio_track.html", identifier_str= identifier_str[0],lyrics =lyrics, nickn=nickn,album=album)
			return render_template("audio_track.html", identifier_str= identifier_str[0],lyrics =lyrics)

		else:
			return render_template("errorSearch.html")
	else:
		return render_template("errorHome.html")
	# if 'nickname' in request.form:
	# else:
		# userid=request.form["nickname"]
		# nickn=userid
		# fdb.hasaccount(userid)
		# lst=fdb.showfavorites(userid)
		# return render_template("login2.html", filename=lst)

# @app.route('/user')
# def home1():
# 	return render_template("user.html")


# @app.route('/user', methods = ["GET", 'POST'])
# def test1():

# 	client = MongoClient()
# 	db = client.db
# 	collection1 = db.test_database

# 	email = request.form["email"]
# 	password = request.form["psw"]

# 	str1 = "your email:" + email + "<br/>" +  "       your password:" + password

# 	k = collection1.find_one({"search_term": "Gloria"})
# 	str1 += k['result']

# 	return str1


if __name__ == "__main__":
	
	app.run(host='0.0.0.0', port=8001, debug=True)




