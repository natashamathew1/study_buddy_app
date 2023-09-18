from django.contrib import admin

from .models import Room, Message, Profile, Class, Event
from django.utils.text import slugify



# Register your models here.



# Register your models here.


#class ProfileAdmin(admin.ModelAdmin):
 #   list_display = ("user", "slug")




##
##
##
##admin.site.register(Room)
##admin.site.register(Message)
##admin.site.register(Profile)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "slug")







admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Class)
admin.site.register(Event)