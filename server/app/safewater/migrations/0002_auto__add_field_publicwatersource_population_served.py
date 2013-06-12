# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PublicWaterSource.population_served'
        db.add_column(u'safewater_publicwatersource', 'population_served',
                      self.gf('django.db.models.fields.IntegerField')(default=0, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PublicWaterSource.population_served'
        db.delete_column(u'safewater_publicwatersource', 'population_served')


    models = {
        u'safewater.publicwatersource': {
            'Meta': {'object_name': 'PublicWaterSource'},
            'contact_addr1': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'contact_addr2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'contact_city': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True'}),
            'contact_org_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'contact_state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'contact_zip': ('django.db.models.fields.CharField', [], {'max_length': '14', 'null': 'True'}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'date_closed': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'epa_region': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'fips_county': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True'}),
            'geography_type': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'owner_type': ('django.db.models.fields.CharField', [], {'max_length': '14', 'null': 'True'}),
            'population_served': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'primary_source': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'primary_source_name': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True'}),
            'pwsid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '9'}),
            'pwstype': ('django.db.models.fields.CharField', [], {'max_length': '7', 'null': 'True'}),
            'regulating_agency_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True'})
        }
    }

    complete_apps = ['safewater']
