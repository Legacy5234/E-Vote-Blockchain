from django.urls import path
from . import views

app_name = 'a_userauthapp'

urlpatterns = [
    path('', views.homepage, name='home'),

    path('create_account/', views.create_account, name='account-create'),    
    path('login_view/', views.login_view, name='login'),
    path('logout_view/', views.logout_view, name='logout'),

    path('home/profile_view/', views.profile_view, name='profile'),
    path('<username>/', views.profile_view, name='userprofile'),
    path('profile/profile_edit/', views.profile_edit, name='profile-edit'),
]