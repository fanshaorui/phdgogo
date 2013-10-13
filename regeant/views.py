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
    results = Regeant.search.query(keyword)
    producers = set()
    for res in results:
        producers.add(res.producer)

    return render_to_response("results.html", RequestContext(
        request, {
            'form': form,
            'keyword': keyword,
            'results': results,
            'producer_quant': len(producers),
            'res_num': len(results)}))


def detail(request, product_pk):
    product = get_object_or_404(Regeant, product_pk)
    return render_to_response("detail.html", RequestContext(
        request, {'product': product}))
