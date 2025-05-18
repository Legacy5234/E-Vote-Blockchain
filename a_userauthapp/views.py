from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from . forms import SignUpForm, ProfileForm
from . models import Voter_User

from django.db import transaction
import uuid 

# Create your views here.
#---------------------------------------------------------------------------------------------------------
# ACCOUNT CREATE VIEW
#---------------------------------------------------------------------------------------------------------
def create_account(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)

        if signup_form.is_valid():

            #Creating User but not saving to database
            user = signup_form.save(commit=False)
            password = signup_form.cleaned_data.get('password')

            #Hashing Password
            user.set_password(password)
            user.is_active = True
            user.save()

            messages.success(request, 'Account Created Successfully..')
            return redirect('a_userauthapp:login')
        else:
            messages.error(request, 'There was an error in creating staff account..')
    else:
        signup_form = SignUpForm()

    context = {
        'signup_form':signup_form,
    }
    return render(request, 'a_userauthapp/create_account.html', context)


#---------------------------------------------------------------------------------------------------------
# LOGIN VIEW
#---------------------------------------------------------------------------------------------------------
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f'Welcome {user.username} to Vote-Chain')
                return redirect('b_voteapp:home')
            else:
                messages.error(request, 'This account has been suspended..')
        else:
            messages.error(request, 'Invalid credentials,Please try again with valid credentials..')
    return render(request, 'a_userauthapp/login.html')


#---------------------------------------------------------------------------------------------------------
# LOGOUT VIEW
#---------------------------------------------------------------------------------------------------------
def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out..')
    return redirect('a_userauthapp:login')


#---------------------------------------------------------------------------------------------------------
# PROFILE VIEW
#---------------------------------------------------------------------------------------------------------
@login_required(login_url='a_userauthapp:login')
def profile_view(request, username=None):
    user = request.user
    if username:
        profile = get_object_or_404(Voter_User, username=username).profile
    else:
        profile = user.profile

    context = {
        'profile':profile,
    }

    return render(request, 'a_userauthapp/profile.html', context)


#---------------------------------------------------------------------------------------------------------
# PROFILE EDIT
#---------------------------------------------------------------------------------------------------------
def profile_edit(request):
    form = ProfileForm(instance=request.user.profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('a_userauthapp:profile')
    context = {
        'form':form,
    }
    return render(request, 'a_userauthapp/profile-edit.html', context)