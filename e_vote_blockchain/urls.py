"""
URL configuration for e_vote_blockchain project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('techpreneur_169/', admin.site.urls),

    path('', include('a_userauthapp.urls')),
    path('', include('b_voteapp.urls')),

    path('home/adminpage/', views.admin_dashboard, name='admin-dashbaord'),
    path('elections/create/', views.create_election, name='create_election'),
    path('candidates/create/', views.create_candidate, name='create_candidate'),

    path('elections/<int:pk>/edit/', views.edit_election, name='edit_election'),
    path('election/<int:pk>/delete/', views.delete_election, name='delete_election'),

    path('candidates/<int:pk>/edit/', views.edit_candidate, name='edit_candidate'),
    path('candidates/<int:pk>/delete/', views.delete_candidate, name='delete_candidate'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
