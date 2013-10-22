# -*- coding: utf-8 -*-

# Create your views here.


from django.core.context_processors import csrf
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from .models import Regeant,Producer
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
    producers_in_session=[]
    for res in pagination.cur_page:
        producers.add(res.producer)
        providers.update(res.producer.providers.all())
    for producer in producers:
	producers_in_session.append(producer.id)
    request.session["producers_in_session"]=producers_in_session
    return render_to_response("results.html", RequestContext(
        request, {
            'form': form,
            'keyword': keyword,
            'results': pagination,
            'producer_quant': len(producers),
	    'producers':producers,
            'provider_quant': len(providers),
            'res_num': pagination.total}))

def producers_provider_all(request):
    producers=[]
    producer_ids=request.session.get("producers_in_session",None)
    if producer_ids:
	for id in producer_ids:
	    producer=Producer.objects.get(id=id)
	    producers.append(producer)
    c=RequestContext(request,locals())
    return render_to_response("provideralldetail.html", c)
def provider_detail(request,producer_pk):
    #print product_pk
    producer = get_object_or_404(Producer,pk=producer_pk)
    c=RequestContext(request,locals())
    return render_to_response("providerdetail.html", c)
def private(request):
    return render_to_response("private.html",RequestContext(request,dict()))