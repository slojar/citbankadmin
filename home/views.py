import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from home.forms import LoginForm

from .api import CitAPI as adminCall


def check_admin_status(user):
    if user.is_staff:
        return True
    else:
        return False


def login_view(request):

    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if not user:
                messages.error(request, 'Login details are not correct')
                return redirect(reverse('home:login'))

            admin = check_admin_status(user)
            if admin is False:
                messages.error(request, 'Only admin users are ALLOWED!!!')
                return redirect(reverse('home:login'))

            login(request, user)
            messages.success(request, f"Welcome {user.username}".title())
            return redirect('home:admin_home')

    context = {
        'form': form,
    }
    return render(request, 'home/login.html', context)


@login_required(login_url='/login')
def home_view(request):
    response = adminCall.get_analytics()
    context = {
        "recent_customers": response["recent_customer"],
        "total_customer": response["total_customer"],
        "airtime_count": response["airtime_count"],
        "data_count": response["data_count"],
        "cable_tv_count": response["cable_tv_count"],
        "airtime_purchase_total": response["airtime_purchase_total"],
        "data_purchase_total": response["data_purchase_total"],
        "cable_tv_purchase_total": response["cable_tv_purchase_total"],
    }
    return render(request, 'home/index.html', context)


def user_logout(request):
    logout(request)
    return redirect('home:login')


@login_required(login_url='/login')
def customer_view(request):
    search = request.POST.get("search")
    account_status = request.POST.get("status")

    if request.method == "POST":
        response = adminCall.get_customers(search=search)
    else:
        response = adminCall.get_customers()

    customer_list = list()

    num = 0
    for customer in response:
        data = dict()
        num += 1

        data["nos"] = num
        data["id"] = customer["id"]
        data["first_name"] = customer["customer_detail"]["first_name"]
        data["last_name"] = customer["customer_detail"]["last_name"]
        data["email"] = customer["customer_detail"]["email"]
        data["username"] = customer["customer_detail"]["username"]
        data["phone_no"] = customer["phone_number"]
        data["status"] = customer["active"]
        customer_list.append(data)

    context = {
        "customers": customer_list
    }
    return render(request, 'home/customer.html', context)


@login_required(login_url='/login')
def customer_detail_view(request, pk):

    if request.method == "POST":
        action = request.POST.get("action")
        detail = adminCall.update_customer(customer_id=pk, active_status=action)

    response = adminCall.get_customer_by_id(pk)
    data = dict()

    dob = response["dob"][:-10]
    joined = response["created_on"][:-22]
    data["last_name"] = response["customer_detail"]["last_name"]
    data["first_name"] = response["customer_detail"]["first_name"]
    data["username"] = response["customer_detail"]["username"]
    data["email"] = response["customer_detail"]["email"]
    data["dob"] = dob
    data["customer_id"] = response["customerID"]
    data["profile_picture"] = response["image"]
    data["bvn"] = response["bvn_number"]
    data["sex"] = response["gender"]
    data["phone_no"] = response["phone_number"]
    data["status"] = response["active"]
    data["date_joined"] = joined
    accounts = list()
    for account in response["accounts"]:
        if account["account_no"]:
            res = dict()
            res["account_no"] = account["account_no"]
            res["acct_type"] = account["account_type"]
            accounts.append(res)

    data["account"] = accounts

    context = {
        "customer": data
    }
    return render(request, 'home/customer_detail.html', context)


@login_required(login_url='/login')
def local_transfer_view(request):
    response = adminCall.get_transfer(transfer_type="local")

    transfers = response["results"]
    transfer_list = list()
    nos = 0
    for transfer in transfers:
        trans_date = transfer["created_on"][:-22]
        nos += 1
        data = dict()
        data["nos"] = nos
        data["sender_f_name"] = transfer["customer"]["first_name"]
        data["sender_l_name"] = transfer["customer"]["last_name"]
        data["customer_id"] = transfer["customer"]["customer_id"]
        data["receiver_name"] = transfer["beneficiary_name"] or "-"
        data["receiver_acct_no"] = transfer["beneficiary_number"] or "-"
        data["status"] = transfer["status"]
        data["amount"] = transfer["amount"]
        data["reference"] = transfer["reference"] or "-"
        data["created_on"] = trans_date
        transfer_list.append(data)

    context = {"transfers": transfer_list}
    return render(request, 'home/local_transfer.html', context)


@login_required(login_url='/login')
def external_transfer_view(request):
    response = adminCall.get_transfer(transfer_type="others")

    transfers = response["results"]
    transfer_list = list()
    nos = 0
    for transfer in transfers:
        trans_date = transfer["created_on"][:-22]
        nos += 1
        data = dict()
        data["nos"] = nos
        data["sender_f_name"] = transfer["customer"]["first_name"]
        data["sender_l_name"] = transfer["customer"]["last_name"]
        data["customer_id"] = transfer["customer"]["customer_id"]
        data["receiver_bank"] = transfer["biller_name"] or "-"
        data["receiver_name"] = transfer["beneficiary_name"] or "-"
        data["receiver_acct_no"] = transfer["beneficiary_number"] or "-"
        data["status"] = transfer["status"]
        data["amount"] = transfer["amount"]
        data["reference"] = transfer["reference"] or "-"
        data["created_on"] = trans_date
        transfer_list.append(data)

    context = {"transfers": transfer_list}
    return render(request, 'home/other_transfer.html', context)
