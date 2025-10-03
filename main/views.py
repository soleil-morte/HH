from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib.auth import authenticate,login,logout 
from django.contrib.auth.decorators import login_required
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


@login_required
def profile_update(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # вернём на просмотр профиля
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'profile_update.html', {'form': form})