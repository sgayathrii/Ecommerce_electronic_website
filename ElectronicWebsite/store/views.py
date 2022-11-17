from django.shortcuts import render
from .models import *

# Create your views here.


def store(request):
	# Changes by Gayathri Dated:16/11/2022
	products = Product.objects.all()
	context = {'products': products}
	return render(request, 'store/store.html', context)

def cart(request):
	# Changes by Gayathri Dated:17/11/2022

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}

	context = {'items':items, 'order':order}
	return render(request, 'store/cart.html', context)

def checkout(request):
	# Changes by Gayathri Dated:17/11/2022
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}
		
	context = {'items':items, 'order':order}
	return render(request, 'store/checkout.html', context)

