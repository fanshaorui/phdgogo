# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Producer'
        db.create_table(u'regeant_producer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('logo_path', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'regeant', ['Producer'])

        # Adding model 'Brand'
        db.create_table(u'regeant_brand', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'regeant', ['Brand'])

        # Adding model 'Regeant'
        db.create_table(u'regeant_regeant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('product_english_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('product_abbr_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('product_abbr_eng_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('product_no', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('cas_no', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('producer_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('producer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fk_regeant_producer', to=orm['regeant.Producer'])),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fk_regeant_brand', blank=True, to=orm['regeant.Brand'])),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modify_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('mass', self.gf('django.db.models.fields.FloatField')(default=0, blank=True)),
            ('mass_unit', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('volumn', self.gf('django.db.models.fields.FloatField')(default=0, blank=True)),
            ('volumn_unit', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('purification', self.gf('django.db.models.fields.FloatField')(default=0, blank=True)),
            ('formation', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('scale_ext1', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('scale_ext2', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('scale_ext3', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('scale_ext4', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('scale_ext5', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('molecular_weight', self.gf('django.db.models.fields.FloatField')(default=0, blank=True)),
            ('molecular_weight_unit', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('molecular_equation', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('moleclar_structure_formation_path', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('ext_attr1', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('ext_attr2', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('ext_attr3', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('ext_attr4', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('ext_attr5', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('references', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('original_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('url_path', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('wiki', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'regeant', ['Regeant'])


    def backwards(self, orm):
        # Deleting model 'Producer'
        db.delete_table(u'regeant_producer')

        # Deleting model 'Brand'
        db.delete_table(u'regeant_brand')

        # Deleting model 'Regeant'
        db.delete_table(u'regeant_regeant')


    models = {
        u'regeant.brand': {
            'Meta': {'object_name': 'Brand'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'regeant.producer': {
            'Meta': {'object_name': 'Producer'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo_path': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'regeant.regeant': {
            'Meta': {'object_name': 'Regeant'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fk_regeant_brand'", 'blank': 'True', 'to': u"orm['regeant.Brand']"}),
            'cas_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'ext_attr1': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'ext_attr2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'ext_attr3': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'ext_attr4': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'ext_attr5': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'formation': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mass': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'mass_unit': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'modify_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'moleclar_structure_formation_path': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'molecular_equation': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'molecular_weight': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'molecular_weight_unit': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'original_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'producer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fk_regeant_producer'", 'to': u"orm['regeant.Producer']"}),
            'producer_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'product_abbr_eng_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'product_abbr_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'product_english_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'product_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'product_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'purification': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'references': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'scale_ext1': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'scale_ext2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'scale_ext3': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'scale_ext4': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'scale_ext5': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'url_path': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'volumn': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'volumn_unit': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'wiki': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['regeant']