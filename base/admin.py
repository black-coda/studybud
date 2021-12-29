from django.contrib import admin
from .models import Room, Topic, Comment


admin.site.register(Room)
admin.site.register(Comment)
admin.site.register(Topic)