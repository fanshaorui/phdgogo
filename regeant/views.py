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
    keyword = request.GET.get('keyword')
    form = SearchForm({'keyword': keyword})
    page_num = int(request.GET.get('page_num', 1))
    pagination = Regeant.page(keyword, page_num=page_num)
    producers = set()
    providers = set()
    for res in pagination.cur_page:
        producers.add(res.producer)
        providers.update(res.producer.providers.all())

    return render_to_response("results.html", RequestContext(
        request, {
            'form': form,
            'keyword': keyword,
            'results': pagination,
            'producer_quant': len(producers),
            'provider_quant': len(providers),
            'res_num': pagination.total}))


def detail(request, product_pk):
    #print product_pk
    product = get_object_or_404(Regeant, pk=product_pk)
    cart_list = request.session.get("cart", None)
    if cart_list is None:
        cart_info = False
        return render_to_response(
            "detail.html", RequestContext(
                request, {'product': product, 'cart_info': cart_info}))
    if product_pk in cart_list:
        cart_info = True
        return render_to_response(
            "detail.html", RequestContext(
                request, {'product': product, 'cart_info': cart_info}))
    else:
        cart_info = False
    return render_to_response(
        "detail.html", RequestContext(
            request, {'product': product, 'cart_info': cart_info}))
