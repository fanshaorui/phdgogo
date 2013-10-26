# -*- coding: utf-8 -*-

from django.core.context_processors import csrf
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from .models import Regeant, Producer
from .forms import SearchForm
import random


def index(request):
    form = SearchForm()
    return render_to_response("index.html", RequestContext(
        request, {'form': form}))


def search(request, target_producer=None):
    keyword = request.GET.get('keyword')
    form = SearchForm({'keyword': keyword})
    page_num = int(request.GET.get('page_num', 1))
    producers = set()
    providers = set()
    pagination_original = Regeant.page(keyword)
    for res in pagination_original.cur_page:
        producers.add(res.producer)
        providers.update(res.producer.providers.all())
    pagination = Regeant.page(
        keyword, page_num=page_num, producer_id=target_producer)
    producers_in_session = []
    for producer in producers:
        producers_in_session.append(producer.id)
        request.session["producers_in_session"] = producers_in_session
    return render_to_response("results.html", RequestContext(
        request, {
            'form': form,
            'keyword': keyword,
            'results': pagination,
            'producer_quant': len(producers),
            'producers': producers,
            'provider_quant': len(providers),
            'res_num': pagination.total,
            'target_producer'=target_produce}))


def producers_provider_all(request):
    producers = []
    producer_ids = request.session.get("producers_in_session", None)
    if producer_ids:
        for id in producer_ids:
            producer = Producer.objects.get(id=id)
            producers.append(producer)
    c = RequestContext(request, locals())
    return render_to_response("provideralldetail.html", c)


def provider_detail(request, producer_pk):
    #print product_pk
    producer = get_object_or_404(Producer, pk=producer_pk)
    c = RequestContext(request, locals())
    return render_to_response("providerdetail.html", c)


def private(request):
    return render_to_response("private.html", RequestContext(request, dict()))


#显示所有生产商入口
def producersshow(request):
    producers = Producer.objects.all()
    products_related = set()
    for i in range(1, 50):
        x = random.randint(5000, 15000)
    try:
        product_related = Regeant.objects.get(pk=str(x))
        products_related.add(product_related)
    except:
        continue
    c = RequestContext(request, locals())
    return render_to_response("product/producersshow.html", c)


#产品详情页
def product_detail(request, pk):
    product = Regeant.objects.get(pk=pk)
    products_related = set()
    for i in range(1, 10):
        x = random.randint(int(pk), int(pk) + 100)
    try:
        product_related = Regeant.objects.get(pk=str(x))
        products_related.add(product_related)
    except:
        continue
    #print products_related
    c = RequestContext(request, locals())
    return render_to_response("product/productdetail.html", c)


#生产商列表页
def producer_product_list(request, pk):
    producer = Producer.objects.get(pk=pk)
    products = Regeant.objects.filter(producer=producer)
    c = RequestContext(request, locals())
    return render_to_response("product/productlist.html", c)
