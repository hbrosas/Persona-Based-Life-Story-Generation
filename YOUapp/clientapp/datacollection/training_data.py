import requests
import time
import pickle
import random
from django.http import JsonResponse
from clientapp.models import TrainingPosts
from clientapp.models import TrainingLikes
from clientapp.models import TrainingEvents
import json

'''
Attached on index.html if collecting training data.
'''

def store_training_data(request):
    print('STORE TRAINING DATA')
    posts = request.POST.get('posts', None)
    likes = request.POST.get('likes', None)
    events = request.POST.get('events', None)

    postsArray = json.loads(posts)[0]
    likesArray = json.loads(likes)[0]
    eventsArray = json.loads(events)[0]

    print('Total Posts: ', len(postsArray))
    print('Total Likes: ', len(likesArray))
    print('Total Events: ', len(eventsArray))

    store_training_posts(postsArray)
    store_training_likes(likesArray)
    store_training_events(eventsArray)

    #dummy data
    data = {
        'success': '123'
    }

    return JsonResponse(data)

def store_training_posts(posts):

    for post in posts:
        fbid = post['id']

        try:
            story = post['story']
        except:
            story = ''

        try:
            description = post['description']
        except:
            description = ''

        try:
            message = post['message']
        except:
            message = ''

        text_post = ''
        space = '. '

        if(story != ''): #e.g. Danica updated her... Danica is at... Danica shared... Danica added...
            text_post += story

        if (description != ''):
            text_post += " The post says " + description + space

        if (message != '' and (description != '' or story!='')):
            text_post += "He says " + message + space
        elif (message != ''):
            text_post += message

        updated_time = post['updated_time']

        p = TrainingPosts(fbid=fbid, post=text_post, updated_time=updated_time)
        p.save()

    print('Text-based posts successfully stored in DB')

def store_training_likes(likes):
    for like in likes:
        fbid = like['id']

        try:
            name = like['name']
        except:
            name = ''

        try:
            category = like['category']
        except:
            category = ''

        try:
            about = like['about']
        except:
            about = ''

        try:
            description = like['description']
        except:
            description = ''

        he_likes = 'He likes '
        space = '. '

        liked_page = he_likes + name + space + about + space + description

        l = TrainingLikes(fbid=fbid, category=category, liked_page=liked_page)
        l.save()

def store_training_events(events):
    for event in events:
        fbid = event['id']

        try:
            name = event['name']
        except:
            name = ''

        try:
            description = event['description']
        except:
            description = ''

        try:
            rsvp_status = event['rsvp_status']
        except:
            rsvp_status = ''

        he_rsvp = 'He is ' + rsvp_status + ' in '        #in or at? -- attending, unsure, interested
        space = '. '

        #e.g. He is attending in Empowher. Empowher is blablabla.
        e = TrainingEvents(fbid=fbid, event=he_rsvp + name + space + description)
        e.save()