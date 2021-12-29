from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomModelForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.object.get(username = username)
        except:
            messages.error(request, 'User does not exist jawe')
        user = authenticate(request, username=username, password=password)  #authenticate user

        if user is not None:
            login(request, user)    #logs user in
        else:
            messages.error(request,'Username or Password not authentic')
    context = {}
    return render(request, 'base/login.html', context)

def logoutView(request):
    logout(request)
    return redirect('home')

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)| Q(host__username__icontains=q) 
        ) #icontains makes it not case-senitive
    topic = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms':rooms,'topics':topic,'room_count':room_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    #returns object according to pk
    rooms = Room.objects.get(id=pk)
    context = {'room':rooms}
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    #Create Room using model form 
    form = RoomModelForm()
    if request.method == 'POST':
        form = RoomModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request,pk):
    #Update room 
    room = Room.objects.get(id=pk)
    # instance of that room
    form = RoomModelForm(instance=room)

    #restrict update to owner of room only
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!!')

    if request.method == 'POST':
        form = RoomModelForm(request.POST, instance=room)

        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/room-update.html', context)

def deleteRoom(request,pk):
    room = Room.objects.get(id = pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})