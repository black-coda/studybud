from django.contrib import admin
from .models import Room, Topic, Comment,Profile


admin.site.register(Room)
admin.site.register(Comment)
admin.site.register(Topic)
admin.site.register(Profile)