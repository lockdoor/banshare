from django.shortcuts import render, redirect
#from django.urls import reverse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse
#from django.core.urlresolvers import reverse

# Create your views here.
def index(request):    
    if not request.user.is_authenticated:
        #return redirect(reverse('share:loginFrom',args=request))
        return loginForm(request)
    else:
        return render(request, 'share/index.html')    

def login(request):    
    if not request.POST['username'] or not request.POST['password']:
        message = 'please insert username and password'
        messages.info(request, message)
        return render(request, 'share/loginForm.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None :
            auth.login(request, user)
            return render(request, 'share/index.html')
        else:
            message = 'username or password wrong'
            messages.info(request, message)            
            return render(request, 'share/loginForm.html')
            

def loginForm(request):
    return render(request, 'share/loginForm.html')

def logout(request):
    auth.logout(request)
    #return redirect(reverse('share:loginFrom'))
    return loginForm(request)
