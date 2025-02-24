from django.shortcuts import redirect, render
from django.http import HttpResponse,JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.

def register(request):
    if request.user.is_authenticated:
        customer = request.user
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        user_not_login = "show"
        user_login = "hidden"
    
    form = CreateUserForm()
    
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    

    context = {'form': form,'user_not_login':user_not_login,'user_login':user_login}
    return render(request, 'app/register.html',context)
def loginPage(request):
    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
        return redirect('home')
    else:
        items = []
        user_not_login = "show"
        user_login = "hidden"
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username or Password is incorrect')

    context = {'user_not_login':user_not_login,'user_login':user_login}
    return render(request, 'app/login.html',context)
def logoutPage(request):
    logout(request)
    return redirect('login')

def home(request):
    if request.user.is_authenticated:
        customer = request.user
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        user_not_login = "show"
        user_login = "hidden"
    context = {'user_not_login':user_not_login,'user_login':user_login}
    return render(request, 'app/home.html',context)

def cart(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'app/cart.html', context)
def saved(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.filter(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'order.get_cart_items':0,'order.get_cart_total':0}
    context = {'items':items,'order':order}
    
    return render(request, 'app/saved.html', context)

