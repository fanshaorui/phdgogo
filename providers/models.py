# -*- coding: utf-8 -*-


from django.db import models

# Create your models here.


class Provider(models.Model):

    ''' Provider model
        @author kid143
        @version 0.0.1
        @since 1.0
    '''

    name = models.CharField(max_length=200)
    address = models.TextField(
        blank=True, null=True, default=None)
    contact = models.TextField(blank=True, default=None)
    site_url = models.URLField(blank=True, null=True, default=None)
    email = models.EmailField(blank=True, null=True, default=None)

    def __unicode__(self):
        return "<Provider: %s>" % self.name


class ProviderProduct(models.Model):

    ''' Provider product model.
        @author kid143
        @version 0.0.1
        @since 1.0
    '''

    name = models.CharField(max_length=255, blank=True)
    eng_name = models.CharField(max_length=255, blank=True)
    product_no = models.CharField(max_length=200, blank=True)
    brand_name = models.CharField(max_length=200, blank=True)
    producer_name = models.CharField(max_length=255, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "<ProviderProduct: %s>" % self.name


class Area(models.Model):

    ''' Area model migrated from shopxx3.
        @author kid143
        @version 0.0.1
        @since 1.0
    '''

    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    orders = models.IntegerField(null=True)
    full_name = models.TextField(blank=True)
    name = models.CharField(max_length=100)
    tree_path = models.CharField(
        max_length=255, null=True, default=None, blank=True)
    parent = models.IntegerField(null=True, blank=True, default=None)

    def get_parent(self):
        return self.__class__.objects.filter(id=self.parent)

    def __unicode__(self):
        return "<Area %s>" % self.name
