# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Provider'
        db.create_table(u'providers_provider', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('address', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
            ('contact', self.gf('django.db.models.fields.TextField')(default=None, blank=True)),
            ('site_url', self.gf('django.db.models.fields.URLField')(default=None, max_length=200, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(default=None, max_length=75, null=True, blank=True)),
        ))
        db.send_create_signal(u'providers', ['Provider'])

        # Adding model 'ProviderProduct'
        db.create_table(u'providers_providerproduct', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('eng_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('product_no', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('brand_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('producer_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'providers', ['ProviderProduct'])

        # Adding model 'Area'
        db.create_table(u'providers_area', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('orders', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('full_name', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('tree_path', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal(u'providers', ['Area'])


    def backwards(self, orm):
        # Deleting model 'Provider'
        db.delete_table(u'providers_provider')

        # Deleting model 'ProviderProduct'
        db.delete_table(u'providers_providerproduct')

        # Deleting model 'Area'
        db.delete_table(u'providers_area')


    models = {
        u'providers.area': {
            'Meta': {'object_name': 'Area'},
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'orders': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'parent': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'tree_path': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'providers.provider': {
            'Meta': {'object_name': 'Provider'},
            'address': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.TextField', [], {'default': 'None', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'default': 'None', 'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'site_url': ('django.db.models.fields.URLField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'providers.providerproduct': {
            'Meta': {'object_name': 'ProviderProduct'},
            'brand_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'eng_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'producer_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'product_no': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['providers']