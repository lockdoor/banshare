from django.urls import path
from . import views
app_name = 'share'
urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('indexWithSetDate/', views.indexWithSetDate, name='indexWithSetDate'),
    path('loginForm/', views.loginForm, name='loginForm'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('customer/', views.customer, name='customer'),
    path('shareGroup/', views.shareGroup, name='shareGroup'),
    path('shareGroup/<int:share_id>/detail/', views.shareDetail, name='shareDetail'),
    path('sharePayDate/', views.sharePayDate, name='sharePayDate'),
    path('addBitInterate/', views.addBitInterate, name='addBitInterate'),
    path('customer/<int:customer_id>/detail/', views.customerDetail, name='customerDetail'),
]