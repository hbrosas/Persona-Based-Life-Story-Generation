from django.db import models
# Create your models here.

class PersonalInformation(models.Model):
    fbid = models.CharField(max_length=50)
    firstname = models.CharField(max_length=250)
    middlename = models.CharField(max_length=250)
    lastname = models.CharField(max_length=250)
    othername = models.CharField(max_length=250)
    gender = models.CharField(max_length=50)
    birthday = models.CharField(max_length=50)
    address = models.TextField()
    numfriends = models.CharField(max_length=10)
    numfollowers = models.CharField(max_length=10)

class WorkAndEducation(models.Model):
    organization = models.TextField()
    type = models.CharField(max_length = 100)
    datestarted = models.CharField(max_length=50)
    dateended = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    courseorposition = models.CharField(max_length=250)

class TestingPosts(models.Model):
    fbid = models.CharField(max_length=50)
    post = models.TextField()
    updated_time = models.TextField()

class TestingLikes(models.Model):
    fbid = models.CharField(max_length=50)
    liked_page = models.TextField()
    category = models.CharField(max_length=100)


class TestingEvents(models.Model):
    fbid = models.CharField(max_length=50)
    event = models.TextField(default=None)

