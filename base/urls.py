from django.urls import path
from .views import deleteMessage, home,logoutView , createRoom, loginView, registerView, room, updateRoom, deleteRoom, userProfile
urlpatterns = [
    path('login/', loginView, name='login'),
    path('register/', registerView, name='register'),
    path('logout/', logoutView, name='logout'),
    path('', home, name='home'),
    path('room/<int:pk>/',room, name='room'),
    path('create-room/',createRoom, name='create-room'),
    path('update-room/<int:pk>/',updateRoom, name='update-room'),
    path('delete-room/<int:pk>/',deleteRoom, name='delete-room'),
    path('delete-message/<int:pk>/',deleteMessage, name='delete-msg'),
    path('userprofile/<int:pk>/',userProfile, name='user_profile'),
]
