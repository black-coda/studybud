from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import Room, Topic, Comment
from .forms import ProfileForm, RoomModelForm, UserModelForm, RegisterForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator

def loginView(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.object.get(username = username)
        except:
            messages.error(request, 'User does not exist jawe')
        user = authenticate(request, username=username, password=password)  #authenticate user

        if user is not None:
            login(request, user)    #logs user in
            return redirect('home')
        else:
            messages.error(request,'Username or Password not authentic')
    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutView(request):
    logout(request)
    return redirect('home')

def registerView(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower() #change username to lowercase
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "An error occured during registration")
    context = {'form':form}
    return render(request, 'base/signup.html',context )

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)| Q(host__username__icontains=q) 
        ) #icontains makes it not case-senitive
    topic = Topic.objects.all()
    topic_count = topic.count()
    room_count = rooms.count()
    room_messages = Comment.objects.filter(
        Q(room__topic__name__icontains=q)
    )[:6]

    #paginator
    # paginator = Paginator(rooms,5) #show 5 rooms per page
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    context = {'rooms':rooms,'topics':topic,'room_count':room_count,'room_messages':room_messages,'topic_count':topic_count,}
    return render(request, 'base/home.html', context)

#@login_required(login_url='login')
def room(request, pk):
    #returns object according to pk
    rooms = Room.objects.get(id=pk)
    comments = rooms.comment_set.all().order_by('created') #query all comment relating to the particular room
    participants = rooms.participants.all()     #query all participants in the group
    #creats an instances of the model Comment // adds to chat
    if request.method == 'POST':
        message = Comment.objects.create(
            user = request.user,
            room = rooms,
            body = request.POST.get('body'),
        )
        rooms.participants.add(request.user)        #add user to the list of particpants in the room
        return redirect('room', rooms.id)

    context = {'room':rooms, 'comments':comments, 'participants':participants}
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    #Create Room using model form 
    form = RoomModelForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        #get or created method checks if the topic already exst or not, if it does
        #it adds to the group

        Room.objects.create(
            host = request.user,    #request.user = host same as if form is valid commit false then assign jhost to the request.user
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        # form = RoomModelForm(request.POST)
        # if form.is_valid():
        #     #assign host to user line 93
        #     room = form.save(commit=False)
        #     room.host = request.user  
        #     room.save()          
        return redirect('home')
    context = {'form':form, 'topics':topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request,pk):
    #Update room 
    room = Room.objects.get(id=pk)
    # instance of that room
    form = RoomModelForm(instance=room)
    topics = Topic.objects.all()
    #restrict update to owner of room only
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        form = RoomModelForm(request.POST, instance=room)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
        # if form.is_valid():
        #     form.save()
        #     return redirect('home')
    context = {'form':form, 'topics':topics,'room':room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})


@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Comment.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed to delete another mans message!!!')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})


def userProfile(request,pk):
    user = User.objects.get(id=pk)
    #To query all the the rooms that is created by the
    rooms = user.room_set.all()
    room_message = user.comment_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'rooms':rooms,'topics':topics,'room_messages':room_message}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def updateUser(request):
    profile_form = ProfileForm(instance=request.user)
    form = UserModelForm(instance=request.user)
    if request.method == 'POST':
        form = UserModelForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('user_profile', pk=request.user.id)
        else:
            messages.error(request, 'Please correct the error!')
    else:
        form = UserModelForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user)
    context = {'form':form,'profile':profile_form}
    return render(request, 'base/update_user.html',context)

@login_required(login_url='login')
def passwordChange(request):
    form = PasswordChangeForm(user=request.user)
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('user_profile', pk=request.user.id)
        else:
            form = PasswordChangeForm()
    context = {'form':form}
    return render(request, 'base/room_form_old.html', context)