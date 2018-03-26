import requests
import time
import pickle
import random
import MySQLdb
import json
from django.http import JsonResponse


def extract_fb_data(request):

    token = request.GET.get('accessToken', None)
    print('access token:' + token)

    graph_url = 'https://graph.facebook.com/v2.11/'
    req_likes_url = 'me?fields=likes{name,category}'

    likes_url = graph_url + req_likes_url

    results = requests.get(likes_url, {'access_token': token})

    return JsonResponse(results.json())

def extract_likes(request):

	access_token_url = "https://graph.facebook.com/oauth/access_token?%20client_id=139479073449755&client_secret=6df56c159ddd907e0089be59b3274358&%20grant_type=client_credentials"
	access_token_json = requests.get(access_token_url)
	data = access_token_json.json()
	access_token = data['access_token']

	graph_url = 'https://graph.facebook.com/v2.11/'
	req = '?fields=name,about,description'

	conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "p@ssword", db = "likesdb", use_unicode=True, charset="utf8mb4")
	cursor = conn.cursor()
	cursor2 = conn.cursor()
	cursor.execute ("select * from likes GROUP BY fbID ORDER BY interest ASC;")
	rows = cursor.fetchall()

	for row in rows:

		print(row[1])
		req_page_url = str(row[3]) + req
		page_url = graph_url + req_page_url
		results = requests.get(page_url, {'access_token': access_token})
		page_data = results.json()

		try:
			name = page_data['name']
		except:
			name = 'page does not exist'

		try:
			fbid = page_data['id']
		except:
			fbid = str(row[3])

		try:
			about = page_data['about']
		except:
			about = ""

		try:
			description = page_data['description']
		except:
			description = ""

		he_likes = 'He likes '
		space = '. '
		story = he_likes + name + space + about + space + description

		cursor2.execute(("INSERT INTO likesdesc(page,story,fbID) VALUES(%s,%s,%s)"), (name, story.encode('unicode-escape'), fbid))
		conn.commit()

