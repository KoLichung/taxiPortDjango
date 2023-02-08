import email
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import authenticate

from modelCore.models import Case

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/backboard/orders')
        else:
            return redirect('/backboard/')

    return render(request, 'backboard/login.html')
    

def logout(request):
    auth.logout(request)
    return redirect('/backboard/')

def orders(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    # 1.取得所需資料(並整理)
    # 2.把所需資料傳到 template 裡面

    cases = Case.objects.all().order_by('-id')

    return render(request,'backboard/orders.html',{'cases':cases})

def order_detail(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    case_id = request.GET.get('case_id')
    case = Case.objects.get(id=case_id)

    return render(request,'backboard/order_detail.html',{'case':case})

def members(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    return render(request,'backboard/members.html')

def member_detail(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    return render(request,'backboard/member_detail.html')

def order_assign_driver(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    return render(request,'backboard/order_assign_driver.html')

def order_driver_status(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    return render(request,'backboard/order_driver_status.html')