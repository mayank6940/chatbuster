# chat/urls.py

from django.urls import path
from .views import join_group, chat, logout_view, profile_page

urlpatterns = [
    path('', join_group, name='join_group'),
    path('chat/', chat, name='chat'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_page, name='profile'),
]
