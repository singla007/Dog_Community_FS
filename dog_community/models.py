from unicodedata import category
from unittest.util import _MAX_LENGTH
from django.db import models


class breed_table(models.Model):
    breed_ID = models.IntegerField()
    breed_name = models.CharField(max_length=255)
    breed_article = models.CharField(max_length=20000)
    breed_image = models.ImageField(upload_to=None)

class dogs_table(models.Model):
    dog_ID = models.IntegerField()
    breed_ID = models.IntegerField()
    is_adopted = models.BooleanField()
    dog_name = models.CharField(max_length=255)
    dog_color = models.CharField(max_length=255)
    dog_age = models.IntegerField()
    is_disable = models.BooleanField()
    diability = models.CharField(max_length=20000)
    unique_identification = models.CharField(max_length=20000)
    is_adoption_ready = models.BooleanField()

class reports_table(models.Model):
    dog_ID = models.IntegerField()
    breed_ID = models.IntegerField()
    reporter_ID = models.IntegerField()
    last_known_location = models.CharField(max_length=20000)
    category = models.CharField(max_length=255)

class user_table(models.Model):
    user_ID = models.IntegerField()
    user_name = models.CharField(max_length=255)
    user_address = models.CharField(max_length=20000)
    user_contact = models.CharField(max_length=255)
    user_email = models.CharField(max_length=255)
class events(models.Model):
    event_ID = models.IntegerField()
    event_location = models.CharField(max_length=20000)
    event_time = models.DateTimeField()
    event_duration = models.IntegerField()
    event_capacity = models.IntegerField()
    event_description = models.CharField(max_length=20000)

class event_subscriptions(models.Model):
    user_ID = models.IntegerField()
    event_Id = models.IntegerField()
    subscription_ID = models.IntegerField()

class admin(models.Model):
    admin_ID = models.IntegerField()
    admin_login_ID = models.CharField(max_length=255)
    admin_login_pass = models.CharField(max_length=255)