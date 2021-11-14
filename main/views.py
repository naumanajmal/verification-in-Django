from django.contrib.messages.api import warning
from verify import settings
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate, login
import uuid
from django.core.mail import send_mail

def home(request):
    return render(request, 'home.html')
def logindef(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(password)

        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.warning(request, 'User not found.')
            return redirect('/login')
        
        
        profile_obj = Profile.objects.filter(user = user_obj ).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return warning('/login')

        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/login')
        login(request, user)
        return redirect('/')

    return render(request , 'login.html') 

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)

        try:
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is taken.')
                return redirect('/register')

            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is taken.')
                return redirect('/register')
            
            user_obj = User(username = username , email = email)
            user_obj.set_password(password)
            user_obj.save()
            token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj , token = token)
            profile_obj.save()
            email_after_registeration(email, token)
            return redirect('/token')

        except Exception as e:
            print(e)


    return render(request , 'register.html') 
def success(request):
    return render(request, 'success.html') 
def token(request):
    return render(request, 'token.html') 
def error(request):
    return render(request, 'error.html') 

def verify(request, token):
    profile_obj = Profile.objects.filter(token = token).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request, 'your account is already verified.')
            return redirect('/accounts/login')
        profile_obj.is_verified = True
        profile_obj.save()
        return redirect('/success')
    else:   
        return redirect('/error')  
def email_after_registeration(email, token):
    subject = 'verification for account'
    message = f'to verify account please click this link http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


