from django.urls import path, include
from .views import *
from django.contrib import admin
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('base/', Base),
    path('auth/register/', Register, name='register'),
    path('auth/login/', Login, name='login'),
    path('logout/', Logout, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', profile_update, name='profile_update'),
    path('auth/', include('allauth.urls')), 
    path('accounts/', include("allauth.urls")),
    path('api/auth/password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('companies/', company_list, name='company_list'),
    path('companies/add/', company_create, name='company_create'),
    path('companies/<int:pk>/', company_detail, name='company_detail'),
    path('companies/<int:pk>/edit/', company_edit, name='company_edit'),
    path('companies/<int:pk>/delete/', company_delete, name='company_delete'),

    path('jobs/', job_list, name='job_list'),
    path('jobs/<int:pk>/', job_detail, name='job_detail'),
    path('jobs/create/', job_create, name='job_create'),
    path('jobs/<int:pk>/edit/', job_edit, name='job_edit'),
    path('jobs/<int:pk>/delete/', job_delete, name='job_delete'),
    
    path('chats/', Chat_list, name='chat_list'),
    path('<int:pk>/', Chat_detail, name='chat_detail'),
     path('message/<int:pk>/edit/', edit_message, name='edit_message'),
    path('message/<int:pk>/delete/', delete_message, name='delete_message'),
]
