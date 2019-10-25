import requests

import urllib.request
import time
from bs4 import BeautifulSoup

import pyrebase
import re
import sys, os

urls = ['http://api.zeit.de/product/zei', 'http://api.zeit.de/product/zede']

HEADER_KEY = "X-Authorization"
API_KEY = "71dca37e2c2f9d8e8e8d0041d665cbff5513bcc2acf7829f6c8c"

all_news = {}

for u in urls:
	print("Getting URLs")
	params = { 'limit': 500}
	r = requests.get(u, headers = {HEADER_KEY: API_KEY}, params = params)
	response = r.json()

	results = response["matches"]

	for res in results:
		newsid = res['uuid']
		newsvalue = res

		if newsid not in all_news:
			all_news[newsid] = newsvalue

for newsid, newsvalue in all_news.items():
	print("Getting News ID")
	try:

		CONTENT_URL = 'http://api.zeit.de/content/' + newsid
		r2 = requests.get(CONTENT_URL, headers = {HEADER_KEY: API_KEY})
		res_data = r2.json()

		categories = res_data['categories']
		creators = res_data['creators']
		keywords = res_data['keywords']

		categories_text = ""
		creators_text = ""
		keywords_text = ""

		for categ in categories:
		    categories_text += ', '.join("{!s}={!r}".format(key,val) for (key,val) in categ.items())
		    categories_text += "$$"
		    
		categories_text = categories_text.strip("$$")

		for crea in creators:
		    creators_text += ', '.join("{!s}={!r}".format(key,val) for (key,val) in crea.items())
		    creators_text += "$$"
		    
		creators_text = creators_text.strip("$$")

		for keyw in keywords:
		    keywords_text += ', '.join("{!s}={!r}".format(key,val) for (key,val) in keyw.items())
		    keywords_text += "$$"
		    
		keywords_text = keywords_text.strip("$$")

		all_news[newsid]['categories_text'] = categories_text
		all_news[newsid]['creators_text'] = creators_text
		all_news[newsid]['keywords_text'] = keywords_text

	except Exception as e:
		_, _, exc_tb = sys.exc_info()
		print("**Error", newsid, str(e), exc_tb.tb_lineno)
		pass

# ---------- Firebase Config Begins ---------- #

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




# ---------- Text Infor Extraction Begins ---------- #

from summa import summarizer

def extract_text_info(text):
    sentences = summarizer.summarize(text,ratio = 0.2)
    sentences = sentences.replace("""\n""", "")
    time_chars = max(int(round(len(sentences.split()) / 200, 0)), 1)
    sentences = sentences.split(".")
    highlight_lines = '$$'.join([str(x) for x in sentences])
    return highlight_lines, time_chars

# ---------- Text Infor Extraction Ends ---------- #




for newsid, newsvalue in all_news.items():
	print("Scraping Data")
	try:
		newsurl = newsvalue['href']
		response = requests.get(newsurl)

		soup = BeautifulSoup(response.text, "html.parser")

		article_image = soup.findAll("img", {"class": "article__media-item"})

		article_image = article_image[0]
		article_image = article_image['src']

		article_text = soup.findAll("div", {"class": "article-page"})
		article_text = article_text[0]
		article_text_html = str(article_text)


		soup = article_text
		for script in soup(["script"]):
		    script.decompose()    # rip it out

		# get text
		text = soup.get_text()

		# break into lines and remove leading and trailing space on each
		lines = (line.strip() for line in text.splitlines())
		# break multi-headlines into a line each
		chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
		# drop blank lines
		fulltext = '\n'.join(chunk for chunk in chunks if chunk)
		fulltext = re.sub('\n+', ' ', fulltext).strip()
		fulltext = ' '.join(fulltext.split())

		all_news[newsid]['image_url'] = article_image
		all_news[newsid]['html_text'] = article_text_html
		all_news[newsid]['full_text'] = fulltext
		all_news[newsid]['complete'] = True

		highlights, timetoread = extract_text_info(fulltext)
		all_news[newsid]['highlights'] = highlights
		all_news[newsid]['timetoread'] = timetoread

		# for k, v in all_news[newsid].items():
		# 	print(k, v)
		# 	print("\n")	

		db.child("all_news").child(newsid).update(all_news[newsid])

	except Exception as e:
		_, _, exc_tb = sys.exc_info()
		print("**Error", newsid, str(e), exc_tb.tb_lineno)
		pass