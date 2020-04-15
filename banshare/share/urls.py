from django.urls import path
from . import views
app_name = 'share'
urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('loginForm/', views.loginForm, name='loginForm'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout')
]