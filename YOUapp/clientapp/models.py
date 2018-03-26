# -*- coding: utf-8 -*-
from django.db import models
# Create your models here.

#from __future__ import unicode_literals
from django.db import models
# Add recognized model option to django

class TrainingPosts(models.Model):
    fbid = models.CharField(max_length=50)
    post = models.TextField()
    updated_time = models.TextField()

class TrainingLikes(models.Model):
    fbid = models.CharField(max_length=50)
    liked_page = models.TextField()
    category = models.CharField(max_length=100)

class TrainingEvents(models.Model):
    fbid = models.CharField(max_length=50)
    event = models.TextField(default=None)
    #rsvp_status = models.CharField(max_length=50)