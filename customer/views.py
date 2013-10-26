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
	#print "cart"
	price=0
	cart=request.session.get("cart",None)
	cart_list=[]
	if not cart:
		cart=[]
		request.session["cart"]=cart
	else:
		cart_list=request.session["cart"]
		skus=[]
		for regeant in cart_list:
			sku=ScalePriceInfo.objects.get(pk=regeant["sku"])
			sku_dict={"sku":sku,"quatity":regeant["quatity"]}
			if sku.currency=="RMB":
				price=price+int(sku.price)*int(regeant["quatity"])
			elif sku.currency=="USD":
				price=price+6.08*int(sku.price)*int(regeant["quatity"])
			#print sku_dict
			skus.append(sku_dict)
	c=RequestContext(request,locals())
	return render_to_response("customer/cart.html",c)

def add_cart(request,pk):
	cart=request.session.get("cart",None)
	if not cart:
		cart=[]
		sku={"sku":pk,"quatity":1}
		cart.append(sku)
		request.session["cart"]=cart
	else:
		for sku_cart in cart:
			if pk==sku_cart["sku"]:
				return cart_view(request)
		sku={"sku":pk,"quatity":1}
		cart.append(sku)
		cart.sort(cmp=lambda x,y:cmp(x["sku"],y["sku"]))
		request.session["cart"]=cart
		print "here"
	return cart_view(request)

def clean_cart(request):
	cart=[]
	request.session["cart"]=cart
	c=RequestContext(request,locals())
	return render_to_response("customer/cart.html",c)

def update_sku(request,pk):
	cart=request.session.get("cart",None)
	if request.method=="POST":
		for item in cart:
			if item["sku"]==pk:
				cart.remove(item)
				item["quatity"]=request.POST["quatity"]
				print item
				cart.append(item)
				request.session["cart"]=cart
				cart.sort(cmp=lambda x,y:cmp(x["sku"],y["sku"]))
	return HttpResponseRedirect(reverse("customer.views.cart_view"))
	

def excelview(request):
	price=0
	cart=request.session.get("cart",None)
	cart_list=[]
	skus=[["药品名称","公司","产品货号","个数","规格","价格","订购时间","订购人"]]
	if not cart:
		cart=[]
		request.session["cart"]=cart
	else:
		cart_list=request.session["cart"]
		for product in cart_list:
			sku_info=ScalePriceInfo.objects.get(pk=product["sku"])
			product_info=[]
			product_info.append(sku_info.product.product_english_name)
			product_info.append(sku_info.product.producer.name)
			product_info.append(sku_info.product.product_no)
			product_info.append(product["quatity"])
			product_info.append(sku_info.scale_info)
			product_info.append(str(sku_info.price)+str(sku_info.currency))
			if sku_info.currency=="RMB":
				price=price+int(sku_info.price)*int(product["quatity"])
			elif sku_info.currency=="USD":
				price=price+6.08*int(sku_info.price)*int(product["quatity"])
			skus.append(product_info)
		product_info=[]
		product_info.append("总价:"+str(price))
		skus.append(product_info)
	return ExcelResponse(skus,"定试剂清单")
