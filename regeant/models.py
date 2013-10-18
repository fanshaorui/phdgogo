# -*- coding: utf-8 -*-


from django.db import models
from scrapy.contrib.djangoitem import DjangoItem
from djangosphinx.models import SphinxSearch
from djangosphinx.apis import current as sphapi
from providers.models import Provider
from .utils import Pagination

# Create your models here.


class Producer(models.Model):

    "Producer model"
    name = models.CharField(max_length=100)
    logo_path = models.URLField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    providers = models.ManyToManyField(
        Provider, related_name='provider_relation_1')

    def __unicode__(self):
        return self.name


class Brand(models.Model):

    "Brand model"
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


class Regeant(models.Model):

    "Regeant record class"
    product_name = models.CharField(max_length=255, blank=True)
    product_english_name = models.CharField(max_length=255, blank=True)
    product_abbr_name = models.CharField(max_length=100, blank=True)
    product_abbr_eng_name = models.CharField(max_length=100, blank=True)
    product_no = models.CharField(max_length=100, blank=True)
    cas_no = models.CharField(max_length=100, blank=True)
    producer_name = models.CharField(max_length=100, blank=True)
    producer = models.ForeignKey(Producer, related_name='fk_regeant_producer')
    brand = models.ForeignKey(
        Brand, related_name='fk_regeant_brand', blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    mass = models.FloatField(blank=True, default=0)
    mass_unit = models.CharField(max_length=10, blank=True)
    volumn = models.FloatField(blank=True, default=0)
    volumn_unit = models.CharField(max_length=10, blank=True)
    purification = models.FloatField(blank=True, default=0)
    formation = models.CharField(max_length=20, blank=True)
    scale_ext1 = models.CharField(max_length=50, blank=True)
    scale_ext2 = models.CharField(max_length=50, blank=True)
    scale_ext3 = models.CharField(max_length=50, blank=True)
    scale_ext4 = models.CharField(max_length=50, blank=True)
    scale_ext5 = models.CharField(max_length=50, blank=True)
    molecular_weight = models.FloatField(blank=True, default=0)
    molecular_weight_unit = models.CharField(max_length=10, blank=True)
    molecular_equation = models.CharField(max_length=100, blank=True)
    moleclar_structure_formation_path = models.URLField(blank=True)
    ext_attr1 = models.CharField(max_length=50, blank=True)
    ext_attr2 = models.CharField(max_length=50, blank=True)
    ext_attr3 = models.CharField(max_length=50, blank=True)
    ext_attr4 = models.CharField(max_length=50, blank=True)
    ext_attr5 = models.CharField(max_length=50, blank=True)
    references = models.TextField(blank=True)
    description = models.TextField(blank=True)
    original_html = models.TextField(blank=True)
    url_path = models.URLField()
    wiki = models.TextField(blank=True)
    search = SphinxSearch(
        index='regeant_regeant',
        weights={
            'product_name': 100,
            'product_english_name': 100,
            'producer_name': 70,
            'product_no': 100,
            'cas_no': 100,
            'product_abbr_name': 100,
            'product_abbr_eng_name': 100,
            'description': 10
        },
        mode='SPH_MATCH_EXTENDED2',
        rankmode='SPH_RANK_SPH04'
    )

    @property
    def product_url(self):
        ''' property method for results page href attributes'''
        return "/product/%s.html" % self.id

    @classmethod
    def page(cls, query_str, page_num=1, per_page=20):
        """return Pagination object"""
        query = cls.search.query(query_str)
        query = query.order_by('-@rank', mode=sphapi.SPH_SORT_EXTENDED)
        return Pagination(query, page_num)

    def __unicode__(self):
        return self.product_name if self.product_name \
            else self.product_english_name


class RegeantItem(DjangoItem):
    django_model = Regeant
