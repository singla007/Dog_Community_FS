from django.db import models

class Breed(models.Model):
    breed_id = models.AutoField(primary_key=True)
    breed_name = models.CharField(max_length=255)
    bred_for = models.CharField(max_length=1000, default="")
    life_span = models.CharField(max_length=1000, default="")
    temperament = models.CharField(max_length=1000, default="")
    origin = models.CharField(max_length=1000, default="")
    breed_image_path = models.ImageField(upload_to='images/breeds', blank=True)
    breed_article = models.CharField(max_length=1024, default="")
    
    def __str__(self):
        return self.breed_name

class Dogs(models.Model):
    dog_id = models.AutoField(primary_key=True)
    breed = models.ForeignKey(Breed, on_delete=models.DO_NOTHING)
    is_adopted = models.BooleanField()
    dog_name = models.CharField(max_length=255)
    dog_color = models.CharField(max_length=255)
    dog_age = models.IntegerField()
    dog_image = models.ImageField(upload_to='images/dogs')
    is_disable = models.BooleanField()
    disabilty = models.CharField(max_length=5000, blank=True)
    unique_identification = models.CharField(max_length=5000)
    is_adoption_ready = models.BooleanField()
    is_featured = models.BooleanField(default=False) # dogs which are loaded without filteration
    
    def __str__(self):
        return self.dog_name

class EventSubscription(models.Model):
    event = models.ForeignKey('Events', on_delete=models.DO_NOTHING)
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.event

class Events(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_location = models.CharField(max_length=5000)
    event_time = models.DateTimeField()
    event_duration = models.IntegerField()
    event_capacity = models.IntegerField()
    event_description = models.CharField(max_length=5000)
    event_image = models.ImageField(upload_to='images/events',default='images/default_event.jpg')
    
    def __str__(self):
        return self.event_location

class Reports(models.Model):
    dog = models.ForeignKey(Dogs, on_delete=models.DO_NOTHING)
    breed = models.ForeignKey(Breed, on_delete=models.DO_NOTHING)
    reporter = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    last_known_location = models.CharField(max_length=5000)
    category = models.CharField(max_length=255)

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=255)
    user_address = models.CharField(max_length=5000, blank=True)
    user_contact = models.CharField(max_length=20)
    user_email = models.EmailField(max_length=255)
    
    def __str__(self):
        return self.user_name

class Adoption(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    dog = models.ForeignKey(Dogs, on_delete=models.DO_NOTHING)

class Admin(models.Model):
    admin_id = models.IntegerField(primary_key=True)
    admin_login_id = models.CharField(max_length=255)
    admin_login_pass = models.CharField(max_length=255)

class Team(models.Model):
    member_id = models.IntegerField(primary_key=True)
    full_name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    member_image = models.CharField(max_length=1024, default="")
    
    def __str__(self):
        return self.full_name

class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    message = models.CharField(max_length = 2000)

    def __str__(self):
        return self.name

class Newsletter(models.Model):
    email = models.EmailField(max_length=255)
    
    def __str__(self):
        return self.email