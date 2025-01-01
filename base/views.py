from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from .models import Room, Topic, Message
from .forms import RoomForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm




# Home view: Displays rooms and topics
def home(request):
    q = request.GET.get('q', '')  # Simplified GET parameter handling
    topics = Topic.objects.filter(name__icontains=q)
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q) )
    context = {
        'rooms': rooms,
        'topics': topics,
        'q': q,
        'room_count': rooms.count(),
        'room_messages':room_messages
    }
    return render(request, 'base/home.html', context)


# Room view: Displays details of a specific room
def room(request, pk, room_messages=None):
    room = get_object_or_404(Room, id=pk)
    participants = room.participants.all()
    if request.method == 'POST':
        messsage = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body'),
        )
        room.participants.add(request.user)
        return redirect('room' , pk=room.id)
    room.messages= room.message_set.all()
    context = {'room': room , 'room_messages': room_messages , 'participants': participants}
    return render(request, 'base/room.html', context)

def userProfile(request, pk ):
    user= User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_message=user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': request.user, 'rooms': rooms , 'room_message': room_message, 'topics': topics}
    return render(request , 'base/profile.html' , context)
# Create Room view: Handles creating a new room

@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


# Update Room view: Handles editing an existing room
@login_required(login_url='login')
def update_room(request, pk):
    room = get_object_or_404(Room, id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed here.')

    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form, 'room': room}
    return render(request, 'base/room_form.html', context)


# Delete Room view: Handles room deletion
@login_required(login_url='login')
def delete_room(request, pk):
    room = get_object_or_404(Room, id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'object': room})


# Login page view using AuthenticationForm
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    context = {'form': form}
    return render(request, 'base/login_register.html', context)


# Login page view using manual authentication
def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # التأكد من وجود المستخدم
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Username not found')
            return redirect('login')  # أعد التوجيه إلى صفحة تسجيل الدخول إذا كان اسم المستخدم غير موجود

        # تحقق من صحة بيانات المستخدم
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect.')  # تحسين رسالة الخطأ

    context={'page':page}
    return render(request, 'base/login_register.html', context)
def registerPage(request):
    form=UserCreationForm()

    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else :
            messages.error(request, 'Username or password is incorrect.')

    return render(request , 'base/login_register.html' , {'form':form})
# Logout view
def logoutUser(request):
    logout(request)
    return redirect('home')
@login_required(login_url='login')
def deleteMessage(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.user == message.user:  # Ensure only the message owner can delete
        message.delete()
        return redirect('home')  # Redirect to an appropriate view
    return HttpResponse("You are not allowed to delete this message")
    return render(request, 'base/delete.html', {'obj': message})























































