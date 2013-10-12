# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from regeant.models import *
from django.http import HttpResponseRedirect
#from regent.views import detail
from django.core.urlresolvers import reverse
from excel_response import ExcelResponse
def cart_view(request):
	print "cart"
	cart=request.session.get("cart",None)
	cart_list=[]
	if not cart:
		cart=[]
		request.session["cart"]=cart
	else:
		cart_list=request.session["cart"]
		products=[]
		for pk in cart_list:
			product=Regeant.objects.get(pk=pk)
			products.append(product)
	c=RequestContext(request,locals())
	return render_to_response("customer/cart.html",c)

def add_cart(request,pk):
	cart=request.session.get("cart",None)
	if not cart:
		cart=[]
		cart.append(pk)
		request.session["cart"]=cart
	else:
		for pk_cart in cart:
			if pk==pk_cart:
				return cart_view(request)
		cart.append(pk)
		request.session["cart"]=cart
		print "here"
	return cart_view(request)

def clean_cart(request):
	cart=[]
	request.session["cart"]=cart
	c=RequestContext(request,locals())
	return render_to_response("customer/cart.html",c)


def excelview(request):
	cart=request.session.get("cart",None)
	cart_list=[]
	products=[["产品名","生产商名称","产品货号"]]
	if not cart:
		cart=[]
		request.session["cart"]=cart
	else:
		cart_list=request.session["cart"]
		for pk in cart_list:
			product=Regeant.objects.get(pk=pk)
			product_info=[]
			product_info.append(product.product_english_name)
			product_info.append(product.producer.name)
			product_info.append(product.product_no)
			products.append(product_info)
	return ExcelResponse(products)
