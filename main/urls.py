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
    path('accounts/', include("allauth.urls")),
    path('api/auth/password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('companies/', company_list, name='company_list'),
    path('companies/add/', company_create, name='company_create'),
    path('companies/<int:pk>/', company_detail, name='company_detail'),
    path('companies/<int:pk>/edit/', company_edit, name='company_edit'),
    path('companies/<int:pk>/delete/', company_delete, name='company_delete'),
]
