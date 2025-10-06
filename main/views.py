from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib.auth import authenticate,login,logout 
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated 
from rest_framework import serializers, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
# from .serializers import CompanySerializer

# Create your views here.
def Base(request):

    return render(request, 'base.html',)


def Register(request):
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            # print(for)
            return redirect('/api/base/')
        
    else:
        form = UserForm()
    
    context={
        'form':form
    }
    return render(request, 'registration/register.html', context)


def Login(request):
    # if request.method == 'POST':
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     form = authenticate(request, username=username, password=password)
    #     if form is not None:
    #         login(request,form)
    #         return redirect('/api/base/')
        return render(request, 'registration/login.html')

def Logout(request):
    logout(request)
    return redirect('/api/base/')


def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})


def profile_update(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # вернём на просмотр профиля
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'profile_update.html', {'form': form})



class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError("Пароли не совпадают.")
        return data


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({"old_password": "Неверный пароль"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password1'])
        user.save()

        return Response({"detail": "Пароль успешно изменён"}, status=status.HTTP_200_OK) 





@login_required
def company_list(request):
    companies = Company.objects.filter(owner=request.user)
    return render(request, 'companies/company_list.html', {'companies': companies})


@login_required
def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk, owner=request.user)
    return render(request, 'companies/company_detail.html', {'company': company})


@login_required
def company_create(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user
            company.save()
            return redirect('company_list')
    else:
        form = CompanyForm()
    return render(request, 'companies/company_form.html', {'form': form, 'title': 'Добавить компанию'})


@login_required
def company_edit(request, pk):
    company = get_object_or_404(Company, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            return redirect('company_detail', pk=pk)
    else:
        form = CompanyForm(instance=company)
    return render(request, 'companies/company_form.html', {'form': form, 'title': 'Редактировать компанию'})


@login_required
def company_delete(request, pk):
    company = get_object_or_404(Company, pk=pk, owner=request.user)
    company.delete()
    return redirect('company_list')

 