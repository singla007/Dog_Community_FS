from django.contrib import admin
from .models import Team, Breed, Dogs, Reports,  ContactUs, Newsletter, User, Adoption, Events, EventSubscription

# Register your models here.
admin.site.register(Team)
admin.site.register(Breed)
admin.site.register(Dogs)
admin.site.register(Reports)
admin.site.register(ContactUs)
admin.site.register(Newsletter)
admin.site.register(User)
admin.site.register(Adoption)
admin.site.register(Events)
admin.site.register(EventSubscription)
