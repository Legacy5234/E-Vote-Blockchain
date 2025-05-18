from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url='a_userauthapp:login')
def admin_dashboard(request):
    return render(request, 'a_userauthapp/admin-page.html')