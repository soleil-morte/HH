from django.contrib.auth.views import LoginView
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
from django.core.exceptions import PermissionDenied
from django.contrib import messages
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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/api/base/')
        else:
            # Добавляем сообщение об ошибке
            messages.error(request, 'Неверное имя пользователя или пароль')
            return render(request, 'registration/login.html', {'error': 'Неверные данные'})
    
    return render(request, 'registration/login.html')

def Logout(request):
    logout(request)
    return redirect('/api/auth/login/')


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



def company_list(request):
    companies = Company.objects.all()  # Все видят все компании
    return render(request, 'companies/company_list.html', {'companies': companies})


def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)
    
    
    return render(request, 'companies/company_detail.html', {'company': company})


@login_required
def company_create(request):
    # Только для работодателей и админов
    if not (request.user.is_employer or request.user.is_superuser):
        raise PermissionDenied("Sizda kompaniya qo‘shish huquqi yo‘q.")

    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user  # Привязываем владельца
            company.save()
            return redirect('company_list')
    else:
        form = CompanyForm()

    return render(request, 'companies/company_form.html', {
        'form': form,
        'title': 'Kompaniya qo‘shish'
    })


@login_required
def company_edit(request, pk):
    company = get_object_or_404(Company, pk=pk)

    # Проверяем, что это владелец компании или админ
    if not (request.user.is_superuser or (request.user.is_employer and company.owner == request.user)):
        raise PermissionDenied("Sizda bu kompaniyani tahrirlash huquqi yo‘q.")

    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            return redirect('company_detail', pk=pk)
    else:
        form = CompanyForm(instance=company)

    return render(request, 'companies/company_form.html', {
        'form': form,
        'title': 'Kompaniyani tahrirlash'
    })


@login_required
def company_delete(request, pk):
    company = get_object_or_404(Company, pk=pk)

    # Только владелец компании или админ может удалить
    if not (request.user.is_superuser or (request.user.is_employer and company.owner == request.user)):
        raise PermissionDenied("Sizda bu kompaniyani o‘chirish huquqi yo‘q.")

    company.delete()
    return redirect('company_list')


def job_list(request):
    jobs = Job.objects.all()  
    return render(request, 'jobs/job_list.html', {'jobs': jobs})


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'jobs/job_detail.html', {'job': job})


@login_required
def job_create(request):
    # Только работодатели и админы
    if not (request.user.is_employer or request.user.is_superuser):
        raise PermissionDenied("Sizda ish e’loni qo‘shish huquqi yo‘q.")

    if request.user.is_superuser:
        # Админ может выбрать любую компанию
        form = JobForm(request.POST or None, request.FILES or None)
    else:
        # Получаем все компании пользователя
        companies = Company.objects.filter(owner=request.user)
        if not companies.exists():
            raise PermissionDenied("Sizda faol kompaniya yo‘q, shuning uchun ish e’loni yarata olmaysiz.")
        
        # Ограничиваем форму только его компаниями
        form = JobForm(request.POST or None, request.FILES or None, user_companies=companies)

    if request.method == 'POST' and form.is_valid():
        job = form.save(commit=False)

        if not request.user.is_superuser:
            # Обычный работодатель — выбираем компанию из формы
            job.company = form.cleaned_data['company']

        job.save()
        form.save_m2m()
        return redirect('job_list')

    return render(request, 'jobs/job_form.html', {
        'form': form,
        'title': 'Ish e’loni qo‘shish'
    })



@login_required
def job_edit(request, pk):
    job = get_object_or_404(Job, pk=pk)

    # Проверка: админ или владелец компании через которую создана вакансия
    if not (request.user.is_superuser or (request.user.is_employer and job.company.owner == request.user)):
        raise PermissionDenied("Sizda bu vakansiyani tahrirlash huquqi yo'q.")

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('job_detail', pk=pk)
    else:
        form = JobForm(instance=job, user=request.user)
    
    return render(request, 'jobs/job_form.html', {'form': form, 'title': 'Редактировать вакансию'})


@login_required
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk)

    # Проверка: админ или владелец компании
    if not (request.user.is_superuser or (request.user.is_employer and job.company.owner == request.user)):
        raise PermissionDenied("Sizda bu vakansiyani o'chirish huquqi yo'q.")

    job.delete()
    return redirect('job_list')


def Chat_list(request):
    chats = Chat.objects.all()
    return render(request, 'chats/chat_list.html', {'chats': chats} )


def Chat_detail(request, pk):
    chats = get_object_or_404(Chat, pk=pk)
    return render(request, 'chats/chat_detail.html', {'chats': chats})