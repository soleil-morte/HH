from django.urls import path, include
from .views import *
from django.contrib import admin

from django.contrib.auth.views import LoginView

urlpatterns = [
    path('base/', Base),
    path('auth/register/', Register, name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('logout/', Logout, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', profile_update, name='profile_update'),
    path('auth/', include('allauth.urls')), 
    path('accounts/', include("allauth.urls"))
]