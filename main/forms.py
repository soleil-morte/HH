from django.contrib.auth.models import User
from django.contrib.auth.forms  import UserCreationForm
from .models import *
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class UserForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r'^\+998\d{9}$',
        message="Telefon raqam +998xxxxxxx fromatida bo'lishi kerak."
    )


    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parol kamida 8 ta simvol'}),
        label='Parol'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parolni tasdiqlash'}),
        label='Parol tasdiqlash'
    )

    class Meta:
        model = User
        fields = ['full_name','phone','email','profile_picture','cv','is_employer', 'username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username kiriting'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Familiya ism sharifini kiriting'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefon raqam kiriting'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email kiriting'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'cv': forms.FileInput(attrs={'class': 'form-control'}),
            'is_employer': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise ValidationError("Parollar mos kelmadi.")
        return cleaned_data
    

class LoginForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parol'})
    )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'phone', 'profile_picture', 'cv', 'is_employer']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'cv': forms.FileInput(attrs={'class': 'form-control'}),
            'is_employer': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'logo', 'description'] 
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Введите название компании'}),
            'description': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Краткое описание компании'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'job_type', 'description', 'salary_min', 'salary_max', 'location']
        widjets = {
            'description': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Краткое описание компании'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nomini kiriting'}),
            'job_type': forms.BooleanField(attrs={'class': 'form-control'}),
            'salary-min': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'salary-max': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
        }