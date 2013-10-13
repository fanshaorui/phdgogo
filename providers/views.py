# -*- coding: utf-8 -*-

import xlrd
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q, Max
from django.http import HttpResponseRedirect
from .forms import *
from .models import *
from regeant.models import *
from django.contrib.auth.decorators import login_required 
from django.core.urlresolvers import reverse
from .forms import ProviderLoginForm,ProviderInfoForm
def register(request):
    if request.method == "POST":
        form = ProviderRegisterForm(request.POST)
        if form.is_valid():
            req_data = form.cleaned_data
            username = req_data['username']
            target = User.objects.filter(
                Q(username__startswith=username) | Q(username__endswith=username))
            if target:
            	print "exist"
                return render_to_response(
                    "providers/register.html",
                    RequestContext(request, dict(msg={
                        'type': 'fail', 'info': 'user already exists!'
                        })))
            else:
            	new_user = User.objects.create_user(username=username, password=req_data['password'])
            	new_user.save()
            	new_provider = Provider(
                	userref=new_user, name=req_data['provider_name'],email=req_data['email'],qqnumber=req_data['qqnumber'],phonenumber=req_data['phonenumber'],contact="",site_url="http://default.com",address="")
            	new_provider.save()
            	auth.logout(request)
            	user_login=auth.authenticate(username=username,password=req_data['password'])
            	if user_login is not None:
					auth.login(request,user_login)
					print "newuser"
            return HttpResponseRedirect(reverse("providers.views.index"))
        else:
        	print "not valid"
        	form = ProviderRegisterForm()
        	return render_to_response("providers/register.html",RequestContext(request,form=form))
    else:
    	print "empty"
        form = ProviderRegisterForm()
        return render_to_response("providers/register.html",RequestContext(request,dict(form=form)))
@login_required
def index(request):
    if request.method=="POST":
		pks=request.POST.getlist("choose")
		provider_self=Provider.objects.get(userref=request.user)
		all_producers=provider_self.provider_relation_1.all()
		for producer in all_producers:
			producer.providers.remove(provider_self)
		for pk in pks:
			Producer.objects.get(pk=pk).providers.add(provider_self)
		producers=Producer.objects.all()
		chosen_producers=provider_self.provider_relation_1.all()
		return render_to_response("providers/index.html",RequestContext(request,dict(producers=producers,chosen_producers=chosen_producers,msg="已修改成功")))
    else:
	    producers=Producer.objects.all()
	    chosen_producers=Provider.objects.get(userref=request.user).provider_relation_1.all()
	    return render_to_response("providers/index.html",RequestContext(request,dict(producers=producers,chosen_producers=chosen_producers)))
def logout_view(request):
	auth.logout(request)
	return HttpResponseRedirect('/')
def login_page(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse("providers.views.index"))
	elif request.method=="POST":
		form=ProviderLoginForm(request.POST)
		if form.is_valid():
			loginform=form.cleaned_data
			username=loginform["username"]
			password=loginform["password"]
			print username,password
			try:
				user=auth.authenticate(username=username,password=password)
				if user is not None:
					auth.login(request,user)
					return HttpResponseRedirect(reverse("providers.views.index"))
				else:
					message="密码错误或者用户名不存在"
					return render_to_response("providers/login.html",RequestContext(request,dict(form=form,message=message)))
			except:
				message="密码错误或者用户名不存在"
				return render_to_response("providers/login.html",RequestContext(request,dict(form=form,message=message)))
		else:
			return render_to_response("providers/login.html",RequestContext(request,dict(form=form)))
	else:
		return render_to_response("providers/login.html",RequestContext(request,dict(form=ProviderLoginForm())))

@login_required
def providerinfo(request):
	if request.method=="POST":
		form=ProviderInfoForm(request.POST)
		if form.is_valid():
			print "newdata"
			clean_form=form.cleaned_data
			changed_user=request.user
			try:
				changed_user.set_password(clean_form["password"])
				changed_user.save()
			except:
				print "user info change error"
				return HttpResponseRedirect(reverse("providers.views.index"))
			provider=Provider.objects.get(userref=request.user)
			provider.phonenumber=clean_form["phonenumber"]
			provider.email=clean_form["email"]
			provider.qqnumber=clean_form["qqnumber"]
			provider.name=clean_form["provider_name"]
			provider.save()
			auth.logout(request)
			user_login=auth.authenticate(username=changed_user.username,password=clean_form["password"])
			auth.login(request,user_login)
			return HttpResponseRedirect(reverse("providers.views.index"))
		else:
			print "wrong post"
			form=ProviderInfoForm(initial={"provider_name":provider.name,"email":provider.email,"phonenumber":provider.phonenumber,"qqnumber":provider.qqnumber})
			return render_to_response("providers/changeinfo.html",RequestContext(request,dict(form=form)))
	else:
		provider=Provider.objects.get(userref=request.user)
		form=ProviderInfoForm(initial={"provider_name":provider.name,"email":provider.email,"phonenumber":provider.phonenumber,"qqnumber":provider.qqnumber})
		return render_to_response("providers/changeinfo.html",RequestContext(request,dict(form=form)))
