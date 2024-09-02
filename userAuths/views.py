from django.shortcuts import render, redirect
from django.urls import reverse

from userAuths.forms import UserRegisterForm, ProfileForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import logout
from .models import  User, Profile
# User = settings.AUTH_USER_MODEL

# Create your views here.

# This view is used for the user registration process, validates and store info into the database
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Hey {username}, Your account was created successfully")
            new_user = authenticate(username=form.cleaned_data['email'], password = form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('core:index')
        else:
            messages.error(request, 'There was an error registering your account')
            return redirect('userAuths:sign-up')
        
    else:
        form = UserRegisterForm()

    context ={
        'form': form
    }
    return render(request, 'userAuths/sign-up.html', context)

# This view is for user that already have an account and want to login
def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are Already logged in!!")

        return redirect('core:index')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
    
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in.")
                return redirect('core:index')
            else:
                messages.warning(request, "User does not exist!")
                return redirect('userAuths:sign-in')
            
        except:
            messages.warning(request, f"User with {email} does not exist!")
            return redirect('userAuths:sign-in')
    else:
        context = {}
        return render(request, 'userAuths/sign-in.html', context)

def profile_edit(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            edited_form = form.save(commit=False)
            edited_form.user= request.user
            edited_form.save()
            messages.success(request, "Profile Updated Successfully.")
            return redirect('core:dashboard')
    else:
        form= ProfileForm(instance=profile)
    context = {
        'form': form
    }
    return render(request, 'userAuths/profile_edit.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, "You have logout!!")

    return redirect('userAuths:sign-in')

def custom_logout_signup(request):
    if request.user.is_authenticated:
        logout(request)  # Log out the user
    return redirect(reverse('userAuths:sign-up'))