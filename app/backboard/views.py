from django.shortcuts import redirect, render
from django.http import HttpResponse

# Create your views here.

def login(request):
    return render(request, 'backboard/login.html')

def orders(request):
    return render(request,'backboard/orders.html')

def order_detail(request):
    return render(request,'backboard/order_detail.html')

def members(request):
    return render(request,'backboard/members.html')

def member_detail(request):
    return render(request,'backboard/member_detail.html')

def order_assign_driver(request):
    return render(request,'backboard/order_assign_driver.html')

def order_driver_status(request):
    return render(request,'backboard/order_driver_status.html')