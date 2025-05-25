from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from . forms import VoterSignupForm, ProfileForm
from . models import Voter_User, Department

from django.http import JsonResponse

from django.db import transaction
import uuid 

# Create your views here.
#---------------------------------------------------------------------------------------------------------
# ACCOUNT CREATE VIEW
#---------------------------------------------------------------------------------------------------------
@login_required(login_url='a_userauthapp:login')
def load_departments(request):
    college_id = request.GET.get('college')
    departments = Department.objects.filter(college_id=college_id).values('id', 'name')
    return JsonResponse(list(departments), safe=False)

@login_required(login_url='a_userauthapp:login')
def create_account(request):
    if request.method == 'POST':
        signup_form = VoterSignupForm(request.POST)

        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            password = signup_form.cleaned_data.get('password')
            role = signup_form.cleaned_data.get('role')

            user.set_password(password)
            user.is_active = True

            if role == 'student':
                user.is_student = True
            elif role == 'staff':
                user.is_staff = True

            user.save()

            messages.success(request, 'Account Created Successfully..')
            return redirect('a_userauthapp:login')
        else:
            messages.error(request, 'There was an error in creating account..')
    else:
        signup_form = VoterSignupForm()

    context = {
        'signup_form': signup_form,
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
@login_required(login_url='a_userauthapp:login')
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save(user=request.user)
            messages.success(request, 'Profile updated successfully.')
            return redirect('a_userauthapp:profile')
    else:
        form = ProfileForm(instance=profile, user=request.user)
    return render(request, 'a_userauthapp/profile-edit.html', {'form': form, 'profile': profile})
