from django.db import models

class Breed(models.Model):
    breed_id = models.AutoField(primary_key=True)
    breed_name = models.CharField(max_length=255)
    breed_article = models.CharField(max_length=10000)
    breed_image_path = models.CharField(max_length=1024)



class Dogs(models.Model):
    dog_id = models.AutoField(primary_key=True)
    breed = models.ForeignKey(Breed, on_delete=models.DO_NOTHING)
    is_adopted = models.BooleanField()
    dog_name = models.CharField(max_length=255)
    dog_color = models.CharField(max_length=255)
    dog_age = models.IntegerField()
    is_disable = models.BooleanField()
    disabilty = models.CharField(max_length=5000)
    unique_identification = models.CharField(max_length=5000)
    is_adoption_ready = models.BooleanField()


class EventSubscriptions(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    event = models.ForeignKey('Events', on_delete=models.DO_NOTHING)
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)


class Events(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_location = models.CharField(max_length=5000)
    event_time = models.DateTimeField()
    event_duration = models.IntegerField()
    event_capacity = models.IntegerField()
    event_description = models.CharField(max_length=5000)


class Reports(models.Model):
    dog = models.ForeignKey(Dogs, on_delete=models.DO_NOTHING)
    breed = models.ForeignKey(Breed, on_delete=models.DO_NOTHING)
    reporter = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    last_known_location = models.CharField(max_length=5000)
    category = models.CharField(max_length=255)


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    field_user_name = models.CharField(max_length=255)
    user_address = models.CharField(max_length=5000)
    user_contact = models.CharField(max_length=20)
    user_email = models.EmailField(max_length=255)

class Admin(models.Model):
    admin_id = models.IntegerField(primary_key=True)
    admin_login_id = models.CharField(max_length=255)
    admin_login_pass = models.CharField(max_length=255)


class Team(models.Model):
    member_id = models.IntegerField(primary_key=True)
    full_name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    

class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    message = models.CharField(max_length = 2000)


class Newsletter(models.Model):
    email = models.EmailField(max_length=255)