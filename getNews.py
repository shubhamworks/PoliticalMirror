# ---------- Firebase Config Begins ---------- #

import pyrebase

firebase_config = {
    "apiKey": "AIzaSyDN9wi_VIbE1lBeg15WFF24j3tyC_F5Agk",
    "authDomain": "medialabhackathon.firebaseapp.com",
    "databaseURL": "https://medialabhackathon.firebaseio.com",
    "projectId": "medialabhackathon",
    "storageBucket": "medialabhackathon.appspot.com",
    "messagingSenderId": "1056171249747",
    "appId": "1:1056171249747:web:eafd3a29b79e996e97f6a6",
    "measurementId": "G-ZJ8YTQ3Z4M"
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

# ---------- Firebase Config Ends ---------- #

# def getPredictCategory(interest):
# 	interest = interest.split(" ")
# 	interest = interest[-5:]
# 	interest = " ".join(interest)

# 	# from tf_recommender import prediction
# 	predicted = prediction(interest)
	
# 	for k, v in predicted.items():
# 		predicted[k] = int(round(v * 10, 0))

# 	return predicted

def getUserFeed():
	response = []
	news = db.child('all_news').get().val()
	userdata = db.child('users').get().val()

	user_interests = userdata['interest']
	user_shown = userdata['shown']
	
	use_prediction = False

	# try:
	# 	predicted = getPredictCategory(user_interests)
	# except:
	# 	use_prediction = False

	# if predicted == None:
	# 	use_prediction = False

	if user_shown != None:
		user_shown = user_shown.split('$$')
	else:
		user_shown = []

	MAX_COUNT = 10
	count = 0
	tmp = []

	for newsid, newsvalue in news.items():
		news_category = newsvalue["news_category"]

		# if (not use_prediction or (news_category in predicted and predicted[news_category] > 0)) and newsid not in user_shown:
		if newsid not in user_shown:
			newsdata = {
				"html_text": newsvalue["html_text"],
				"highlights": newsvalue["highlights"],
				"image_url": newsvalue["image_url"],
				"timetoread": newsvalue["timetoread"],
				"release_date": newsvalue["release_date"],
				"title": newsvalue["title"],
				"subtitle": newsvalue["subtitle"],
				"news_category": newsvalue["news_category"],
				"prediction": use_prediction,
				"newsurl": newsvalue["href"]
			}
			response.append(newsdata)
			tmp.append(newsid)

			count += 1
			# predicted[news_category] -= 1
			if count == MAX_COUNT:
				break

	if len(user_shown) >= 100:
		user_shown = tmp
	else:
		user_shown += tmp

	user_shown = "$$".join(user_shown)
	# db.child('users').update({"shown": shown})
	return response

# response = getUserFeed()
# for t in response:
# 	print(t['news_category'])

# --------- Flask Code Begins --------- #

#!flask/bin/python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/getFeed')
def solve():
	try:
		response = getUserFeed()
		result = jsonify({
			'result': response,
			'status': 'ok',
			'code': 200
		})
		result.headers.add('Access-Control-Allow-Origin', '*')
	except Exception as e:
		print(str(e))
		result = jsonify({
			'status': 'fail',
			'code': 500
		})
		result.headers.add('Access-Control-Allow-Origin', '*')

	return result

@app.route('/postFeedback', methods = ['POST'])
def savedata():
	postdata = request.json
	user_interest = db.child("users").child("interest").get().val()
	user_interest += " " + postdata["news_category"]

	db.child("users").update({"interest": user_interest})

	return jsonify({
		'status': 'ok',
		'code': 200
	})

if __name__ == '__main__':
    app.run()

# --------- Flask Code Ends --------- #