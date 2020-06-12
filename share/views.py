from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse
#from django.utils import timezone
import datetime
import json
from .models import Customers, Share_groups, Share_groups_customers, Share_pay_date
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='share:loginForm')
def index(request):
    toDay = datetime.datetime.now()
    #toDay = toDay.replace(day=18)
    #toDay = toDay.replace(month=6)
    showToDay = Share_pay_date.objects.filter(pay_date__day=toDay.day, pay_date__month=toDay.month, pay_date__year=toDay.year) 
    context = {'toDay':toDay, 'showToDay': showToDay}
    return render(request, 'share/index.html', context)


@login_required(login_url='share:loginForm')
def indexWithSetDate(request):
    toDay = request.POST['date']
    print(type(toDay), toDay)
    toDay = datetime.datetime.strptime(toDay, '%Y-%m-%d')
    #print(type(toDay), toDay)
    
    showToDay = Share_pay_date.objects.filter(pay_date__day=toDay.day, pay_date__month=toDay.month, pay_date__year=toDay.year) 
    context = {'toDay':toDay, 'showToDay': showToDay}
    return render(request, 'share/indexWithSetDate.html', context)

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
    shares = Share_groups.objects.filter(share_close=False)    
    return render(request, 'share/shareGroup.html', {'shares': shares})


@login_required(login_url='share:loginForm')
def shareDetail(request, share_id):
    share = Share_groups.objects.get(pk=share_id)
    shareGenre = str(int(share.admin_frist)) + str(int(share.admin_last)) + str(int(share.date_receive_no_payment)) + str(int(share.queue)) + str(int(share.fix_rate)) + str(int(share.bit)) + str(int(share.fix_last_date))
    arr = [' เท้าแชร์ยกหัว ', ' เท้าแชร์หักค้ำท้าย ', ' หักวันรับ ', ' รับตามมือจอง ', 'ฟิกเรต', ' บิท ', ' วันที่ส่งต้องลงท้ายตรงกัน ']
    shareDescription = shareGenre
    for index, letter in enumerate(shareGenre):
        if letter == '1':            
            shareDescription += arr[index]
    print(shareDescription)
    context = {'share': share, 'shareDescription':shareDescription}
    return render(request, 'share/detail'+shareGenre+'.html', context)

@login_required(login_url='share:loginForm')
def sharePayDate(request):    
    payDates = json.loads(request.POST['myJson'])    
    Share_groups.objects.filter(pk=payDates[1]['group']).update(build_share_pay_date=False)
    for queue in payDates:        
        share = Share_groups_customers.objects.get(share_group=queue['group'], receive_queue=queue['queue'])
        if share.share_group.bit == False:
            date = datetime.datetime.strptime(queue['date'], '%d,%b,%Y')
            share.receive_date = date
            share.save()
        for date in payDates:
            date = datetime.datetime.strptime(date['date'], '%d,%b,%Y')
            share.share_pay_date_set.create(pay_date=date)
    share = Share_groups.objects.get(pk=payDates[1]['group'])
    return redirect(reverse('share:index'))
    
@login_required(login_url='share:loginForm')
def addBitInterate(request):
    share_groups_customer_id = request.POST['share_groups_customer_id']
    interest_bit = request.POST['addBitInterate']
    share_group_id = request.POST['share_group_id']
    share_groups_customers_receive_queue = request.POST['share_groups_customer_receive_queue']
    share_groups_customers_receive_date = request.POST['share_groups_customer_receive_date']
    queue = request.POST['queue']
    date = datetime.datetime.strptime(share_groups_customers_receive_date, '%d,%b,%Y')
    
    if share_groups_customers_receive_queue != queue:
        swap = Share_groups_customers.objects.get(share_group=share_group_id,receive_queue=queue)
        swap.receive_queue=0
        swap.save()
        insert_bit = Share_groups_customers.objects.get(id=share_groups_customer_id)
        receive_queue_swap = insert_bit.receive_queue    
        insert_bit.receive_queue = queue
        insert_bit.receive_date = date
        insert_bit.interest_bit = interest_bit
        insert_bit.save()
        swap.receive_queue=receive_queue_swap
        swap.save() 
    else:
        insert_bit = Share_groups_customers.objects.get(id=share_groups_customer_id)        
        insert_bit.receive_queue = queue
        insert_bit.receive_date = date
        insert_bit.interest_bit = interest_bit
        insert_bit.save()
    print(share_groups_customers_receive_queue, share_groups_customers_receive_date)   
    return redirect('share:shareDetail', share_id = share_group_id)
    
def customerDetail(request, customer_id):
    customer = Customers.objects.get(pk=customer_id)
    toDay = datetime.datetime.now()
    #print(toDay)
    context = {'customer':customer, 'toDay':toDay}
    return render(request, 'share/customerDetail.html', context)