import requests
import time
import pickle
import random
from django.http import JsonResponse


def extract_fb_data(request):

    token = request.GET.get('accessToken', None)
    print('access token:' + token)

    graph_url = 'https://graph.facebook.com/v2.11/'
    req_likes_url = 'me?fields=likes{name,category}'

    likes_url = graph_url + req_likes_url

    results = requests.get(likes_url, {'access_token': token})

    return JsonResponse(results.json())