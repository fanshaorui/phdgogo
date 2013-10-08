# -*- coding: utf-8 -*-


# Create your views here.


import xlrd
from django.core.context_processors import csrf
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q
from .forms import *
from .models import *


def upload_product_list(request):
    if request.method == "POST":
        uploaded = request.FILES[0]
        filename = uploaded.name
        with open('/tmp/' + filename, 'wb') as to_save:
            for chunk in uploaded.chunks:
                to_save.write(chunk)

        data = xlrd.open_workbook('/tmp/' + filename)
        table = data.sheets()[0]
        for i in range(table.nrows):
            row_data = table.row_values(i)
            producer, product_no, name, eng_name = row_data
            target = ProviderProduct.objects.filter(
                producer_name=producer, product_no=product_no)
            if target:
                continue
            new_product = ProviderProduct(
                name=name, eng_name=eng_name,
                product_no=product_no, producer_name=producer)
            new_product.save()
        return render_to_response(
            "uploaded_success.html",
            RequestContext(request, info="Upload Success!"))
    else:
        form = UploadForm()
        render_to_response("upload_form.html", RequestContext(
            request, {'form': form}))


def provider_submit(request):
    if request.method == "POST":
        form = ProviderInfoForm(request.POST)
        req_data = form.cleaned_data
        prov_name = req_data['name']
        target = Provider.objects.get(
            Q(name__startswith=prov_name) | Q(name__endswith=prov_name))
        if target:
            return render_to_response(
                "exists.html", RequestContext(request, form=form))

        new_provider = Provider(
            name=prov_name,
            address=req_data.get('address'),
            contact=req_data.get('contact'),
            site_url=req_data.get('site_url'),
            email=req_data.get('email'))
        new_provider.save()

        return render_to_response(
            "submit_success.html",
            RequestContext(request, provider=new_provider))
    else:
        form = ProviderInfoForm()
        render_to_response(
            "provider_input.html", RequestContext(request, form=form))
