from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Registration,Room,Message
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login

# Create your views here.
def registration(request):
    if request.method == 'POST':
        profile_pic = request.FILES['profilePic']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']
        
        if password != confirm_password:
            messages.error(request,'Passwords are not matching')
            return redirect('registration')
            
        if User.objects.filter(username=username).exists():
            messages.error(request,'Username already exists')
            return redirect('registration')
            
        else:
            user = User.objects.create_user(username=username,password=password)
            user.save()
            regitered_user = Registration(user=user, profile_pic=profile_pic)
            regitered_user.save()
            user = authenticate(username=username,password=password)
            auth_login(request,user)
            return redirect('home')

    return render(request,'registration.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            auth_login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Invalid credentials')
            return redirect('login')
    return render(request,'login.html')

def get_room_name(user1_id, user2_id):
    ids = sorted([str(user1_id), str(user2_id)])
    return f'chat_{ids[0]}_{ids[1]}'

def home(request):
    current_user = request.user
    current_user_profile = Registration.objects.get(user=current_user)
    other_users = Registration.objects.exclude(user=current_user)

    chat_with_id = request.GET.get('chat_with')
    chat_messages = []
    selected_user = None
    room = None

    if chat_with_id:
        try:
            selected_user = User.objects.get(id=chat_with_id)
            room_name = get_room_name(current_user.id, selected_user.id)
            room, _ = Room.objects.get_or_create(name=room_name)

            # Get all messages in the room
            chat_messages = Message.objects.filter(room=room).order_by('created')
        except User.DoesNotExist:
            pass  # Or handle error appropriately

    return render(request, 'home.html', {
        'current_user': current_user,
        'current_user_profile': current_user_profile,
        'other_users': other_users,
        'selected_user': selected_user,
        'chat_messages': chat_messages,
        'room_name': room.name if room else None,
    })