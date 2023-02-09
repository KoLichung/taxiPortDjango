import email
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import authenticate
import urllib

from modelCore.models import Case, User

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
    
    users = User.objects.filter(is_staff=False).order_by('-id')

    return render(request,'backboard/members.html',{'users':users})

def member_detail(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    user_id = request.GET.get('user_id')
    user = User.objects.get(id=user_id)

    cases = Case.objects.filter(user=user)


    return render(request,'backboard/member_detail.html',{'user':user, 'cases':cases})

def order_assign_driver(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    if request.method == 'POST':
        case_id = request.POST.get('case_id')
        driverName = request.POST.get('driverName')
        case_carNumberid = request.POST.get('carNumber')
        carModel = request.POST.get('carModel')
        minutesToArrive = request.POST.get('minutesToArrive')

        case = Case.objects.get(id=case_id)
        case.driver_name = driverName
        case.car_model = carModel
        case.car_id_number = case_carNumberid
        case.expect_minutes = minutesToArrive

        case.case_state = 'way_to_catch'
        case.save()

        return redirect_with_params('order_driver_status',{'case_id':case_id})

    case_id = request.GET.get('case_id')
    case = Case.objects.get(id=case_id)

    return render(request,'backboard/order_assign_driver.html',{'case':case})

def order_driver_status(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    if request.method == 'POST':
        case_id = request.POST.get('case_id')
        case_status = request.POST.get('button_submit')
        case = Case.objects.get(id=case_id)

        # 用了 way_to_catch, catched, finished
        if case.case_state == 'way_to_catch' and case_status == 'catched':
            case.case_state = 'catched'
        elif case.case_state == 'catched' and case_status == 'finished':
            case.case_state = 'finished'

        case.save()
        return redirect('order_driver_status')

    case_id = request.GET.get('case_id')
    case = Case.objects.get(id=case_id)

    return render(request,'backboard/order_driver_status.html',{'case':case})

def redirect_with_params(url, params=None):
    response = redirect(url)
    if params:
        query_string = urllib.parse.urlencode(params)
        response['Location'] += '?' + query_string
    return response