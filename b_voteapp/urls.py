from django.urls import path
from . import views

app_name = 'b_voteapp'

urlpatterns = [
    path('', views.homepage, name='home'),
    path('elections/<int:pk>/', views.election_detail, name='election_detail'),
    
    path('cast_vote/', views.cast_vote, name='cast_vote'),
]