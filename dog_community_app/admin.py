from django.contrib import admin
from .models import Team, Breed, Dogs, Reports,  ContactUs, Newsletter

# Register your models here.
admin.site.register(Team)
admin.site.register(Breed)
admin.site.register(Dogs)
admin.site.register(Reports)
admin.site.register(ContactUs)
admin.site.register(Newsletter)
