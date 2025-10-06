from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib.auth import authenticate,login,logout 
from django.contrib.auth.decorators import login_required
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
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
    