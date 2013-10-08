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
    url(r'/index.html', 'regeant.views.index'),
    url(r'/search/', 'regeant.views.search'),
    url(r'product/(\w+).html', 'regeant.views.detail')
)
