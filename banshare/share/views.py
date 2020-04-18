from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from .models import Customers, Share_groups, Share_groups_customers
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='share:loginForm')
def index(request):
    '''if not request.user.is_authenticated:
        return redirect(reverse('share:loginForm'))
    else:
        return render(request, 'share/index.html', {'thistime': timezone.now()})'''
    return render(request, 'share/index.html', {'thistime': timezone.now()})


def login(request):
    if not request.POST['username'] or not request.POST['password']:
        message = 'please insert username and password'
        messages.info(request, message)
        return render(request, 'share/loginForm.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            # return render(request, 'share/index.html')
            return redirect(reverse('share:index'))
        else:
            message = 'username or password wrong'
            messages.info(request, message)
            return render(request, 'share/loginForm.html')


def loginForm(request):
    return render(request, 'share/loginForm.html')


def logout(request):
    auth.logout(request)
    return redirect(reverse('share:index'))
    # return loginForm(request)


@login_required(login_url='share:loginForm')
def customer(request):
    customers = Customers.objects.all()
    return render(request, 'share/customer.html', {'customers': customers})


@login_required(login_url='share:loginForm')
def shareGroup(request):
    shares = Share_groups.objects.all()
    return render(request, 'share/shareGroup.html', {'shares': shares})


@login_required(login_url='share:loginForm')
def shareDetail(request, share_id):
    share = Share_groups.objects.get(pk=share_id)
    shareGenre = str(int(share.admin_frist)) + str(int(share.admin_last)) + str(int(share.queue)) + str(int(share.bit))
    arr = [' เท้าแชร์ยกหัว ', ' เท้าแชร์หักค้ำท้าย ', ' รับตามมือจอง ', ' บิท ']
    shareDescription = ''
    for index, letter in enumerate(shareGenre):
        if letter == '1':            
            shareDescription += arr[index]
    print(shareDescription)
    context = {'share': share, 'shareDescription':shareDescription}
    return render(request, 'share/detail'+shareGenre+'.html', context)



