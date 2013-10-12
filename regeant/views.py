# -*- coding: utf-8 -*-

# Create your views here.


from django.core.context_processors import csrf
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from .models import Regeant
from .forms import SearchForm


def index(request):
    form = SearchForm()
    return render_to_response("index.html", RequestContext(
        request, {'form': form}))


def search(request):
    keyword = request.cleaned_data['keyword']
    form = SearchForm({'keyword': keyword})
    results = Regeant.search.query(keyword)
    return render_to_response("results.html", RequestContext(
        request, {
            'form': form,
            'results': results,
            'res': len(results)}))


def detail(request,product_pk):
    #print product_pk
    product = get_object_or_404(Regeant,pk=product_pk)
    cart_list=request.session.get("cart",None)
    if cart_list is None:
    	cart_info=False
    	return render_to_response("detail.html", RequestContext(request, {'product': product,'cart_info':cart_info}))
    if product_pk in cart_list:
    	cart_info=True
    	return render_to_response("detail.html", RequestContext(request, {'product': product,'cart_info':cart_info}))
    else:
    	cart_info=False
    return render_to_response("detail.html", RequestContext(request, {'product': product,'cart_info':cart_info}))
