# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'search_demo.views.home', name='home'),
    # url(r'^search_demo/', include('search_demo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^private/$','regeant.views.private'),#隐私权政策
    url(r'search/(\w+)', 'regeant.views.search'),#搜索结果页
    url(r'search/', 'regeant.views.search'),#搜索结果页
    url(r'providerdetail/(\w+)/', 'regeant.views.provider_detail'),#产品供应商详情页
    url(r'propro/','regeant.views.producers_provider_all'),#
    url(r'^provider/$', 'providers.views.index'),#供应商后台首页
    url(r'^provider/info/$','providers.views.providerinfo'),#供应商信息页
    url(r'^accounts/logout/$','providers.views.logout_view'),#退出登陆
    url(r'^accounts/login_page/$','providers.views.login_page'),#供应商登陆
    url(r'^providers/register/$','providers.views.register'),#供应商注册
    url(r'customer/cart/view/','customer.views.cart_view'),#用户采购清单
    url(r'^customer/cart/add/(\d+)/$','customer.views.add_cart'),#采购清单添加
    url(r'customer/cart/clean/','customer.views.clean_cart'),#清空采购清单
    url(r'customer/cart/excel/','customer.views.excelview'),#采购清单导出excel
    url(r'', 'regeant.views.index'),#首页
)
