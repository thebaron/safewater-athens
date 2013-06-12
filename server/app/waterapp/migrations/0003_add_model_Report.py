# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Report'
        db.create_table(u'waterapp_report', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=16, null=True)),
            ('source_uri', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('report_type', self.gf('django.db.models.fields.CharField')(max_length=16, null=True)),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('date_reported', self.gf('django.db.models.fields.DateField')(null=True)),
            ('date_resolved', self.gf('django.db.models.fields.DateField')(null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('verification', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('severity', self.gf('django.db.models.fields.CharField')(max_length=16, null=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True)),
            ('info_url1', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('info_url2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('info_url3', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('info_url4', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('pws_affected', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['waterapp.PublicWaterSource'])),
            ('contaminant_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('contaminant_type', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('violation_type', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
        ))
        db.send_create_signal(u'waterapp', ['Report'])


    def backwards(self, orm):
        # Deleting model 'Report'
        db.delete_table(u'waterapp_report')


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
            'population_served': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'primary_source': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'primary_source_name': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True'}),
            'pwsid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '9'}),
            'pwstype': ('django.db.models.fields.CharField', [], {'max_length': '7', 'null': 'True'}),
            'regulating_agency_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True'})
        },
        u'waterapp.report': {
            'Meta': {'object_name': 'Report'},
            'contaminant_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'contaminant_type': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'date_reported': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'date_resolved': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info_url1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'info_url2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'info_url3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'info_url4': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'pws_affected': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['waterapp.PublicWaterSource']"}),
            'report_type': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'severity': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'source_uri': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'verification': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'violation_type': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'})
        }
    }

    complete_apps = ['waterapp']
