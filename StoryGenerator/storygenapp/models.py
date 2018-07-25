from django.db import models

# Create your models here.
class PersonalInformation(models.Model):
    fbid = models.CharField(max_length=50)
    name = models.CharField(max_length=500)
    gender = models.CharField(max_length=50)
    birthday = models.CharField(max_length=50)
    address = models.TextField()
    location = models.TextField()
    hometown = models.TextField()
    about = models.TextField()
    numfriends = models.CharField(max_length=10)

    class Meta:
        db_table = "profile"

class WorkAndEducation(models.Model):
    fbid = models.CharField(max_length=50)
    organization = models.TextField()
    type = models.CharField(max_length = 100)
    yearstarted = models.CharField(max_length=50)
    yearended = models.CharField(max_length=50)
    courseorposition = models.TextField()

    class Meta:
        db_table = "work_and_education"

class AssertionTypes(models.Model):
    user_pref = models.CharField(max_length=250)
    assertion_type = models.CharField(max_length=250)
    parameter = models.CharField(max_length=500)

    class Meta:
        db_table = "assertions_types"

class Assertions(models.Model):
    user_pref = models.CharField(max_length=250)
    assertion_type = models.IntegerField()
    parameters = models.TextField()

    class Meta:
        db_table = "assertions"