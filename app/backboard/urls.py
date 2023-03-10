from django.urls import path, include
from . import views
from django.shortcuts import render
from django.http import HttpResponse

urlpatterns = [
    path('', views.login, name='login'),
    path('logout', views.logout, name='backboard_logout'),
    path('orders', views.orders, name = 'orders'),
    path('reserve_orders', views.reserve_orders, name = 'reserve_orders'),
    path('order_detail', views.order_detail, name = 'order_detail'), 
    path('members', views.members, name = 'members'), 
    path('member_detail', views.member_detail, name = 'member_detail'), 
    path('order_assign_driver', views.order_assign_driver, name = 'order_assign_driver'), 
    path('order_driver_status', views.order_driver_status, name = 'order_driver_status'), 
]