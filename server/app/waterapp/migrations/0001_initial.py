# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PublicWaterSource'
        db.create_table(u'waterapp_publicwatersource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('pwsid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=9)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('epa_region', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('geography_type', self.gf('django.db.models.fields.CharField')(max_length=9, null=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('county', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('fips_county', self.gf('django.db.models.fields.CharField')(max_length=5, null=True)),
            ('regulating_agency_name', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=6, null=True)),
            ('date_closed', self.gf('django.db.models.fields.DateField')(null=True)),
            ('pwstype', self.gf('django.db.models.fields.CharField')(max_length=7, null=True)),
            ('primary_source', self.gf('django.db.models.fields.CharField')(max_length=3, null=True)),
            ('primary_source_name', self.gf('django.db.models.fields.CharField')(max_length=45, null=True)),
            ('owner_type', self.gf('django.db.models.fields.CharField')(max_length=14, null=True)),
            ('contact_name', self.gf('django.db.models.fields.CharField')(max_length=70, null=True)),
            ('contact_org_name', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('contact_phone', self.gf('django.db.models.fields.CharField')(max_length=15, null=True)),
            ('contact_addr1', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('contact_addr2', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('contact_city', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('contact_state', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('contact_zip', self.gf('django.db.models.fields.CharField')(max_length=14, null=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'waterapp', ['PublicWaterSource'])


    def backwards(self, orm):
        # Deleting model 'PublicWaterSource'
        db.delete_table(u'waterapp_publicwatersource')


    models = {
        u'waterapp.publicwatersource': {
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

    complete_apps = ['waterapp']