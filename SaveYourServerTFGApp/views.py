from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm
from .forms import UserForm
from .forms import FileForm

from .models import *


@login_required(login_url='login')
def index(request):

    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your file has been updated succesfully')
            return redirect('index')


    else:
        form = FileForm()


    context = {'form': form}
    return render(request, 'SaveYourServerTFGUsersApp/index.html', context)

@login_required(login_url='login')
def file_list(request):
    files = File.objects.all()

    context = {'files': files}
    return render(request, 'SaveYourServerTFGUsersApp/file_list.html', context)


@login_required(login_url='login')
def view_data(request, pk):

    user_update = MyUser.objects.get(id=pk)
    form = UserForm(instance=user_update)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user_update)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {'form': form}
    return render(request, 'SaveYourServerTFGUsersApp/view_data.html', context)

def deleteUser(request, pk):
    user_delete = MyUser.objects.get(id=pk)

    if request.method == 'POST':
        user_delete.delete()
        return redirect('index')

    context = {'item': user_delete}
    return render(request, 'SaveYourServerTFGUsersApp/delete.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            dni = request.POST.get('dni')
            password = request.POST.get('password')

            user = authenticate(request, dni=dni, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'Dni OR Password is incorrect')

    context={}
    return render(request, 'SaveYourServerTFGUsersApp/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('full_name')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

    context={'form': form}
    return render(request, 'SaveYourServerTFGUsersApp/register.html', context)


@login_required(login_url='login')
def who_are_we(request):
    return render(request, 'SaveYourServerTFGUsersApp/who_are_we.html')

@login_required(login_url='login')
def privacity(request):
    return render(request, 'SaveYourServerTFGUsersApp/privacity.html')

@login_required(login_url='login')
def terms(request):
    return render(request, 'SaveYourServerTFGUsersApp/terms.html')

@login_required(login_url='login')
def how_it_works(request):
    return render(request, 'SaveYourServerTFGUsersApp/how_it_works.html')

@login_required(login_url='login')
def notification(request):
    notifications = Notification.objects.all()

    context = {'notifications': notifications}
    return render(request, 'SaveYourServerTFGUsersApp/notification_list.html')


@login_required(login_url='login')
def show_notification(request, notification_id):

    n = Notification.objects.get(id=notification_id)

    context={'notification': n}
    return render(request, 'SaveYourServerTFGUsersApp/notification.html', context)


@login_required(login_url='login')
def delete_notification(request, notification_id):

    n = Notification.objects.get(id=notification_id)
    n.is_visualized = True
    n.save()

    context={'notification': n}
    return render(request, 'SaveYourServerTFGUsersApp/index.html', context)
    



