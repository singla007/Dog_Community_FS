from django.contrib import admin
from .models import Team, Breed, Dogs

# Register your models here.
admin.site.register(Team)
admin.site.register(Breed)
admin.site.register(Dogs)
