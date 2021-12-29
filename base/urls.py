from django.urls import path
from .views import home,logoutView , createRoom, loginView, room, updateRoom, deleteRoom
urlpatterns = [
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    path('', home, name='home'),
    path('room/<int:pk>/',room, name='room'),
    path('create-room/',createRoom, name='create-room'),
    path('update-room/<int:pk>/',updateRoom, name='update-room'),
    path('delete-room/<int:pk>/',deleteRoom, name='delete-room'),
]
