from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder
from .forms import *
from django.contrib.auth.forms import UserCreationForm

from django.core.mail import EmailMessage
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import Group
from django.template.loader import render_to_string
from django.forms import inlineformset_factory

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse
from django.views.generic import TemplateView, ListView

# Create your views here.

def store(request):
	# Changes by Gayathri Dated:16/11/2022 --- Tongmei 17/11
	
	data = cartData(request)
	cartItems = data['cartItems']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def cart(request):
	# Changes by Gayathri Dated:17/11/2022  Tongmei 17/11 18/11

	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order,'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	# Changes by Gayathri Dated:17/11/2022 and Tongmei 17/11 18/11
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order,'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

# Changes by Tongmei 17/11
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)
#--------Changes by Gayathri--------------#


@login_required
def logoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse('store'))

#----------------------#

# Tongmei test -- Login & logout & register & passwordReset --  11/20 
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username, password=password)


            if user is not None:
                login(request, user)
                return redirect('store')
            else:
                messages.info(request, 'Username OR password is incorrect')

    context  = {}
    return render(request, 'store/login.html', context)

def registerPage(request):

    if request.user.is_authenticated:
        return redirect('store')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                Customer.objects.create(
                    user=user,
                    name=user.username,
                    email = user.email,
                    )

                username = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + username)

                return redirect('store:login')

        context = {'form': form,}
        return render(request, 'store/register.html', context)
    
#View for search.html
def searchResultView(request):
	if request.method == 'POST':
		search = request.POST['search']
		products = Product.objects.filter(name__contains=search)
		return render(request, 'store/Search_products.html', {'search':search, 'products':products})
	else:
		return render(request, 'store/Search_products.html', {})


	
    